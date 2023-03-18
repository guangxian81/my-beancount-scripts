import calendar
import csv
import re
from zipfile import ZipFile
from datetime import date
from io import BytesIO, StringIO

import dateparser
from beancount.core import data
from beancount.core.data import Note, Transaction

from ..accounts import accounts
from . import (DictReaderStrip, get_account_by_guess,
               get_income_account_by_guess, replace_flag)
from .base import Base
from .deduplicate import Deduplicate

Account零钱通 = 'Assets:Flow:EBank:光的微信'
Account工商银行 = 'Assets:Flow:Bank:光工商银行'
Account收入红包 = 'Income:Life:红包'
Account支出红包 = 'Expenses:Life:Other:红包'
Account余额 = 'Assets:Flow:EBank:光的微信'


class WaCaiIn(Base):

    def __init__(self, filename, byte_content, entries, option_map):
        # if re.search(r'微信支付账单.*\.zip$', filename):
        #     password = input('微信账单密码：')
        #     z = ZipFile(BytesIO(byte_content), 'r')
        #     z.setpassword(bytes(password, 'utf-8'))
        #     filelist = z.namelist()
        #     if len(filelist) == 2 and re.search(r'微信支付.*\.csv$', filelist[1]):
        #         byte_content = z.read(filelist[1])
        if re.match("WaCaiIn.*",filename) == None:
            raise RuntimeError('Not WaCaiIn Trade Record!')
        print('Import WaCai: ')
        fid = open(filename,'r',encoding="utf-8")
        data = csv.reader(fid)
        lines =list()
        i = 0
        for row in data:
            tmp =''
            if i == 0:
                print('len(row'+str(len(row)))
            i=i+1
            for sstr in row:
                tmp = tmp + sstr + ','
            lines.append(tmp)
        # content = csv.DictReader(filename)
        # lines = content

        print('Import WeChat: ' + lines[0])
        content = "\n".join((lines[0:len(lines)]))
        # print('haah'+content)
        print('haah done')
        self.content = content
        self.deduplicate = Deduplicate(entries, option_map)

    def parse(self):
        content = self.content
        f = StringIO(content)
        reader = DictReaderStrip(f, delimiter=',')
        transactions = []
        i = 0
        for row in reader:
            if i == 0:
                print('yug'+str(row))
            i=i+1
            print("Importing {} at {}".format(row['收入大类'], row['收入日期']))
            meta = {}
            time = dateparser.parse(row['收入日期'])
            # meta['wechat_trade_no'] = row['交易单号']
            # meta['trade_time'] = row['交易时间']
            # meta['timestamp'] = str(time.timestamp()).replace('.0', '')
            account = get_account_by_guess(row['收入大类'],row['账户'], time)
            flag = "*"
            amount_string = row['收入金额'].replace('¥', '')
            amount = float(amount_string)

            # if row['商户单号'] != '/':
            #     meta['shop_trade_no'] = row['商户单号']

            # if row['备注'] != '/':
            #     meta['note'] = row['备注']

            meta = data.new_metadata(
                'beancount/core/testing.beancount',
                12345,
                meta
            )
            entry = Transaction(
                meta,
                date(time.year, time.month, time.day),
                '*',
                row['收入大类'],
                row['收入大类']+'@@'+row['账户']+"@@"+row['备注'],
                data.EMPTY_SET,
                data.EMPTY_SET, []
            )

            status = row['币种']
            # 消费
            if status == '人民币' :
                # if '早餐' in row['支出小类']:
                #     entry = entry._replace(payee='')
                #     entry = entry._replace(narration='零钱花费')
                #     data.create_simple_posting(
                #         entry, Account零钱通, amount_string, 'CNY')
                # elif '工商银行(4794)' in row['账户']:
                #     entry = entry._replace(payee='')
                #     entry = entry._replace(narration='工商银行')
                #     data.create_simple_posting(
                #         entry, Account零钱通, amount_string, 'CNY')
                # else:
                    # if '微信红包' in row['账户']:
                    #     account = Account支出红包
                    #     if entry.narration == '/':
                    #         entry = entry._replace(narration=row['账户'])
                    # else:
                account = get_account_by_guess(
                    row['账户'], row['账户'], time)
                # if account == "Unknown":
                #	entry = replace_flag(entry, '!')
                data.create_simple_posting(
                entry, account, amount_string, 'CNY')
                data.create_simple_posting(
                    entry, accounts[row['收入大类']], None, None)
            # elif row['当前状态'] == '已存入零钱' or row['当前状态'] == '已收钱':
            #     if '微信红包' in row['账户']:
            #         if entry.narration == '/':
            #             entry = entry._replace(narration=row['账户'])
            #         data.create_simple_posting(entry, Account收入红包, None, 'CNY')
            #     else:
            #         income = get_income_account_by_guess(
            #             row['交易对方'], row['商品'], time)
            #         if income == 'Income:Unknown':
            #             entry = replace_flag(entry, '!')
            #         data.create_simple_posting(entry, income, None, 'CNY')
            #     data.create_simple_posting(
            #         entry, Account余额, amount_string, 'CNY')
            else:
                print('Unknown row', row)

            # 收入
            # 转账
            #b = printer.format_entry(entry)
            # print(b)
            if not self.deduplicate.find_duplicate(entry, amount, 'wechat_trade_no'):
                transactions.append(entry)

        self.deduplicate.apply_beans()
        return transactions
