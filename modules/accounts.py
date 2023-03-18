import re

import dateparser


def get_eating_account(from_user, description, time=None):
    if time == None or not hasattr(time, 'hour'):
        return 'Expenses:Food:零食'
    elif time.hour <= 3 or time.hour >= 21:
        return 'Expenses:Food:零食'
    elif time.hour <= 10:
        return 'Expenses:Food:早餐'
    elif time.hour <= 16:
        return 'Expenses:Food:午餐'
    else:
        return 'Expenses:Food:晚餐'


def get_credit_return(from_user, description, time=None):
    for key, value in credit_cards.items():
        if key == from_user:
            return value
    return "Unknown"


public_accounts = [
    'Assets:Company:Alipay:StupidAlipay'
]

credit_cards = {
    '中信银行': 'Liabilities:CreditCard:CITIC',
    '工商银行(4794)':'Assets:Bank:光工商银行 ',
    '招商银行':'Assets:Bank:光招商银行 ',
    '中国银行':'Assets:Bank:光中国银行 ',
}

accounts = {
    '商品房':'Assets:Fixed:商品房 ',
    '股票':'Assets:Invest:股票 ',
    '自定义基金':'Assets:Invest:自定义基金 ',
    '定期':'Assets:Invest:定期 ',
    '黄金':'Assets:Invest:黄金 ',
    '光的支付宝':'Assets:EBank:光的支付宝 ',
    '婵的支付宝':'Assets:EBank:婵的支付宝 ',
    '光的微信':'Assets:EBank:光的微信 ',
    '零钱':'Assets:EBank:光的微信 ',
    '婵的微信':'Assets:EBank:婵的微信 ',
    '现金':'Assets:Flow:现金 ', 
    '工商银行(4794)':'Assets:Bank:光工商银行 ',
    '工行储蓄卡':'Assets:Bank:光工商银行 ',
    '家庭储蓄':'Assets:EBank:家庭储蓄 ',
    '婵的储蓄':'Assets:EBank:婵的储蓄 ',
    '娃的储蓄':'Assets:EBank:娃的储蓄 ',
    '光的公积金':'Assets:EBank:光的公积金 ',
    '婵的公积金':'Assets:EBank:婵的公积金 ',
    '家庭消费':'Assets:EBank:家庭消费 ',
    '装修费用':'Assets:EBank:装修费用',
    '购房储蓄':'Assets:EBank:购房储蓄',
    '婵的消费':'Assets:EBank:婵的储蓄',
    '公交':'Assets:Flow:公交',
    '招行信用卡':'Liabilities:CreditCard:招商信用卡',
    '工行信用卡':'Liabilities:CreditCard:工行信用卡',
    '中行储蓄卡':'Assets:Bank:光中国银行',
    '苏行储蓄卡':'Assets:Bank:光苏州银行',
    '光的消费':'Assets:EBank:光的微信',
    '交行信用卡':'Liabilities:CreditCard:交行信用卡',
    '招行储蓄卡':'Assets:Bank:光招商银行',
    '理财收益':'Income:Invest:理财',
    '红包':'Income:Life:红包',
    '报销款':'Income:Work:报销',
    '工资薪水':'Income:Work:工作收入',
    '福利补贴':'Income:Work:工卡补贴',
    '退款返款':'Income:Life:其他',
    '兼职外快':'Income:Life:其他',
    '漏记款':'Income:Life:其他',
    '赠送':'Income:Life:其他',
    '还钱':'Income:Life:其他',
    '礼金':'Income:Life:红包',
    '零花钱':'Income:Life:其他',
    '理财':'Income:Invest:投资收益',
    '生活费':'Income:Life:其他',
    '应收款':'Income:Life:其他',
    '利息':'Income:Life:其他',
    '租金':'Income:Life:其他',
    '营业收入':'Income:Life:其他',
    '赔付款':'Income:Life:其他',
    '销售款':'Income:Life:其他',
    '退款':'Income:Life:其他',
    '其他':'Income:Life:其他',
    '奖金':'Income:Work:工作收入',
    '倪家':'Assets:Bank:倪家',


    'YS股票':'Expenses:Life:其他',
    '财付通':'Expenses:Life:其他',
    '小婵':'Assets:Bank:小婵',
    '信用卡':'Assets:Bank:信用卡',
}

descriptions = {
    #'滴滴打车|滴滴快车': get_didi,
    '余额宝.*收益发放': 'Income:Invest:余额宝收益',
    '转入到余利宝': 'Assets:EBank:光的支付宝',
    '信用卡自动还款|信用卡还款': get_credit_return,
    '外卖订单': get_eating_account,
    '美团订单': get_eating_account,
    '地铁出行': 'Expenses:Travel:公交地铁',
    '火车票': 'Expenses:Travel:火车',
    '装修':'Expenses:Life:装修',
    '水果':'Expenses:Food:水果',
    '零食':'Expenses:Food:零食',
    '午餐':'Expenses:Food:午餐',
    '晚餐':'Expenses:Food:晚餐',
    '地铁':'Expenses:Travel:公交地铁',
    '公交':'Expenses:Travel:公交地铁',
    '日常百货':'Expenses:Shopping:购物',
    '卡费':'Expenses:Life:手续费',
    '早餐':'Expenses:Food:早餐',
    '宵夜':'Expenses:Food:零食',
    '家居':'Expenses:Life:装修',
    '饮料':'Expenses:Food:饮料',
    '打车':'Expenses:Travel:出租车',
    '礼金':'Expenses:Other:红包',
    '红包':'Expenses:Other:红包',
    '礼物':'Expenses:Other:红包',
    '保健品':'Expenses:Shopping:药品',
    '电器':'Expenses:Life:装修',
    '饰品':'Expenses:Shopping:首饰',
    '食材':'Expenses:Food:零食',
    '押金':'Expenses:Life:手续费',
    '话费':'Expenses:Subscribe:宽带话费',
    '水费':'Expenses:Life:水电燃气',
    '电费':'Expenses:Life:水电燃气',
    '护肤品':'Expenses:Shopping:购物',
    '贷款':'Liabilities:Cycle:房贷',
    '房租':'Expenses:Life:房租',
    '自行车':'Expenses:Travel:共享单车',
    '充电':'Expenses:Life:手续费',
    '按摩':'Expenses:Hobby:运动',
    '健身':'Expenses:Hobby:运动',
    '衣服':'Expenses:Shopping:衣服鞋帽',
    '燃气费':'Expenses:Life:水电燃气',
    '化妆品':'Expenses:Shopping:化妆品',
    '鞋子':'Expenses:Shopping:衣服鞋帽',
    '培训':'Expenses:Hobby:图书',
    '买药':'Expenses:Shopping:药品',
    '课程':'Expenses:Hobby:图书',
    '火车':'Expenses:Travel:火车',
    '住宿':'Expenses:Life:房租',
    '汽车':'Expenses:Travel:公交地铁',
    '公交卡':'Expenses:Travel:公交地铁',
    '手续费':'Expenses:Life:手续费',
    '书籍':'Expenses:Hobby:图书',
    '网费':'Expenses:Subscribe:宽带话费',
    '门票':'Expenses:Hobby:旅游',
    '电影':'Expenses:Hobby:电影',
    '请客':'Expenses:Life:其他',
    '检查':'Expenses:Shopping:药品',
    '利息':'Expenses:Hobby:图书',
    '小费':'Expenses:Life:其他',
    '理发':'Expenses:Hobby:理发',
    '网吧':'Expenses:Life:其他',
    '棋牌':'Expenses:Life:其他',
    '旅游':'Expenses:Hobby:旅游',
    '丢失':'Expenses:Life:其他',

    'YS股票':'Expenses:Life:其他',
    '财付通':'Expenses:Life:其他',
    '婵的储蓄':'Assets:EBank:婵的储蓄 ',
    '光的支付宝':'Assets:EBank:光的支付宝 ',
    '婵的支付宝':'Assets:EBank:婵的支付宝 ',
    '光的微信':'Assets:EBank:光的微信 ',
    '零钱':'Assets:EBank:光的微信 ',
    '婵的微信':'Assets:EBank:婵的微信 ',
    '家庭储蓄':'Assets:EBank:家庭储蓄 ',
    '婵的储蓄':'Assets:EBank:婵的储蓄 ',
    '娃的储蓄':'Assets:EBank:娃的储蓄 ',
    '光的公积金':'Assets:EBank:光的公积金 ',
    '婵的公积金':'Assets:EBank:婵的公积金 ',
    '购房储蓄':'Assets:EBank:购房储蓄',
    '工行信用卡':'Liabilities:CreditCard:工行信用卡',
    '家庭储蓄':'Assets:EBank:家庭储蓄 ',
    '家庭消费':'Assets:EBank:家庭消费 ',
    '光的消费':'Assets:EBank:光的微信',
    '装修费用':'Assets:EBank:装修费用',
    '招行信用卡':'Liabilities:CreditCard:招商信用卡',
    '中行储蓄卡':'Assets:Bank:光中国银行',
    '工行储蓄卡':'Assets:Bank:光工商银行 ',
    '倪家':'Assets:Bank:倪家',
    '小婵':'Assets:Bank:小婵',
    '信用卡':'Liabilities:CreditCard:信用卡',
    '现金':'Assets:Flow:现金 ', 
    '招行储蓄卡':'Assets:Bank:光招商银行',
    '理财收益':'Assets:Invest:理财收益'


}

anothers = {
    '上海拉扎斯': get_eating_account
}

incomes = {
    '余额宝.*收益发放': 'Income:Invest:余额宝收益',
}

description_res = dict([(key, re.compile(key)) for key in descriptions])
another_res = dict([(key, re.compile(key)) for key in anothers])
income_res = dict([(key, re.compile(key)) for key in incomes])
