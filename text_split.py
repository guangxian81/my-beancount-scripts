import re ,os


# fid = open("expense.bean","r",encoding = "utf-8")
# fid = open("income.bean","r",encoding = "utf-8")
fid = open("sw.bean","r",encoding = "utf-8")
wfile_pre 	=	None
wfid_pre 	=	None
wfile_cur 	=	None
wfid_cur 	=	None

for row in fid.readlines():
	matchfid = re.search("\d\d\d\d-\d\d",row)

	if matchfid 	!= None: #找到带有日期的行
		wfile_cur 	=	matchfid.group(0)

		if wfile_cur !=	wfile_pre:#和上个日期行不一致
			if wfid_cur != None:	#关闭上个文件
				wfid_cur.close()
			wfile_pre = wfile_cur

			wfid_cur = open(wfile_cur+".bean",'a+',encoding="utf-8")

			wfid_cur.write(row)
		else:	#写不是新日期的日期行
			wfid_cur.write(row) 
	else:#写不是日期行
		if wfid_cur != None:
			wfid_cur.write(row)


