# coding=utf-8


import urllib
#from datetime import datetime
import datetime
import time

#2015年5月8日这是系统上最早能查到的数据
start_date=datetime.date(2015,5,8)
now_date = datetime.datetime.now().date()

local_date_4_file=time.strftime('%Y%m%d',time.localtime(time.time()-24*60*60))
out_file="c:\\IBM-9\\ChinaClear4Customer"+"_"+local_date_4_file+".csv"


f=open(out_file,'w')
print >>f,"Up_to_date",",","1.XinZengShu",",","1.1.XinZeng_ZiRanRen",",","1.1.XinZeng_Fei_ZiRanRen",",",\
"2.QiMoShu",",","2.1.QiMoShu_ZiRanRen",",","2.1.1.QiMoShu_ZiRanRen_A",",","2.1.2.QiMoShu_ZiRanRen_B",",","2.2.QiMoShu_Fei_ZiRanRen",",","2.2.1.QiMoShu_Fei_ZiRanRen_A",",","2.2.2.QiMoShu_Fei_ZiRanRen_B",",",\
"3.QiMoChiCangShu",",","3.1.QiMoChiCangShu_A",",","3.2.QiMoChiCangShu_B",",",\
"4.CanYuJiaoYiShu",",","4.1.CanYuJiaoYiShu_A",",","4.2.CanYuJiaoYiShu_B"

tmp_date=start_date
url_part_1="http://www.chinaclear.cn/cms-search/view.action?action=china&viewType=&dateStr="
url_part_2="&channelIdStr="

#可以查询指定日期证劵发行及登记情况（channelIdStr=535b821c09eb424a818b82a2364caf74）
# http://www.chinaclear.cn/cms-search/view.action?action=china&viewType=&dateStr=2016.01.16&channelIdStr=535b821c09eb424a818b82a2364caf74
#这个535b821c09eb424a818b82a2364caf74代码可以在http://www.chinaclear.cn/cms-search/view.action?action=china&viewType=&dateStr=2016.01.16&channelIdStr=的源码中中看到
#有很多是没数据的比如“一周基金账户情况”
'''
					     <select name = "channelIdStr" id = "channelIdStr" >

					     		<option value = "6ac54ce22db4474abc234d6edbe53ae7"  selected>
					     			一周投资者情况统计表
					     		</option>

					     		<option value = "db99d614c00342558b02e35239e7e495"  >
					     			一周股票账户情况
					     		</option>

					     		<option value = "db876d23a22c480386b751ae099e9909"  >
					     			一周基金账户情况
					     		</option>

					     		<option value = "dc96df3a8d7b440cbe1abbeb87dab715"  >
					     			开户情况
					     		</option>

					     		<option value = "535b821c09eb424a818b82a2364caf74"  >
					     			证劵发行及登记
					     		</option>

					     		<option value = "c416e4b7bc6742ecb96c866231224751"  >
					     			证劵过户及代发现金红利
					     		</option>

					     		<option value = "21e71d6f9d324a82a63944ea66ea9fb9"  >
					     			资金结算
					     		</option>
'''


while tmp_date<now_date:
    #第一次检测到自然人是“新增”，第二次是“期末”
    num_ZiRanRen=0
    #第一次检测到非自然人是“新增”，第二次是“期末”
    num_Fei_ZiRanRen=0
    #第一次检测到"已开立A股账户投资者"是“自然人_已开立A股账户投资者”，第二次是“非自然人_已开立A股账户投资者”
    num_Yi_KaiLi_A=0
    #第一次检测到"已开立B股账户投资者"是“自然人_已开立B股账户投资者”，第二次是“非自然人_已开立B股账户投资者”
    num_Yi_KaiLi_B=0

    url_all=url_part_1+str(tmp_date.year)+"."+str(tmp_date.month)+"."+str(tmp_date.day)+url_part_2
    page=urllib.urlopen(url_all)
    html=page.read()
    html_line=html.splitlines()

    for i in range(0,len(html_line)):
        #注意是中文（
        if html_line[i].find("一周投资者情况统计表（")>0:
            tmp=html_line[i].split("-")
            #注意是中文）
            tmp=tmp[1].split("）")
            Up_to_date=tmp[0]
            continue

        #针对变态的全部数据写在一行
        if len(html_line[i])>200:
            #尼玛！网页源码看到是小写p，但收到的竟然是大写P
            if html_line[i].find("</p>")>0:
                to_analyse=html_line[i].split("</p>")
            #2016.7.1之前用的是大写/P
            elif html_line[i].find("</P>")>0:
                to_analyse=html_line[i].split("</P>")

            for a in range(0,len(to_analyse)):
                if to_analyse[a].find("一、新增投资者数量")>0:
                    tmp=to_analyse[a+1].split(">")
                    tmp=tmp[4].split("<")
                    XinZengShu=tmp[0].replace(",","")
                    continue

                #"非自然人"这个必须放在"自然人"之前判断，否则永远无机会轮到"非自然人"
                if to_analyse[a].find("非自然人")>0:
                    num_Fei_ZiRanRen=num_Fei_ZiRanRen+1
                    tmp=to_analyse[a+1].split(">")
                    tmp=tmp[4].split("<")
                    if num_Fei_ZiRanRen==1:
                        XinZengShu_Fei_ZiRanRen=tmp[0].replace(",","")
                    elif num_Fei_ZiRanRen==2:
                        QiMoShu_Fei_ZiRanRen=tmp[0].replace(",","")
                    continue

                if to_analyse[a].find("自然人")>0:
                    num_ZiRanRen=num_ZiRanRen+1
                    tmp=to_analyse[a+1].split(">")
                    tmp=tmp[4].split("<")
                    if num_ZiRanRen==1:
                        XinZengShu_ZiRanRen=tmp[0].replace(",","")
                    elif num_ZiRanRen==2:
                        QiMoShu_ZiRanRen=tmp[0].replace(",","")
                    continue


                if to_analyse[a].find("二、期末投资者数量")>0:
                    tmp=to_analyse[a+1].split(">")
                    tmp=tmp[4].split("<")
                    QiMoShu=tmp[0].replace(",","")
                    continue

                #2016年7月1日之前是大写；之后就变成小写，够变态了吧！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
                if to_analyse[a].find("已开立<span>A</span>股账户投资者")>0 or  to_analyse[a].find("已开立<SPAN>A</SPAN>股账户投资者")>0:
                    num_Yi_KaiLi_A=num_Yi_KaiLi_A+1
                    tmp=to_analyse[a+1].split(">")
                    tmp=tmp[4].split("<")
                    if num_Yi_KaiLi_A==1:
                        QiMoShu_ZiRanRen_A=tmp[0].replace(",","")
                    elif num_Yi_KaiLi_A==2:
                        QiMoShu_Fei_ZiRanRen_A=tmp[0].replace(",","")
                    continue

                #够变态了吧！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
                if to_analyse[a].find("已开立<span>B</span>股账户投资者")>0 or to_analyse[a].find("已开立<SPAN>B</SPAN>股账户投资者")>0:
                    num_Yi_KaiLi_B=num_Yi_KaiLi_B+1
                    tmp=to_analyse[a+1].split(">")
                    tmp=tmp[4].split("<")
                    if num_Yi_KaiLi_B==1:
                        QiMoShu_ZiRanRen_B=tmp[0].replace(",","")
                    elif num_Yi_KaiLi_B==2:
                        QiMoShu_Fei_ZiRanRen_B=tmp[0].replace(",","")
                    continue

                if to_analyse[a].find("期末持仓投资者数量")>0:
                    tmp=to_analyse[a+1].split(">")
                    tmp=tmp[4].split("<")
                    QiMoChiCangShu=tmp[0].replace(",","")
                    continue

                if to_analyse[a].find("持有<span>A</span>股的投资者")>0 or to_analyse[a].find("持有<SPAN>A</SPAN>股的投资者")>0 :
                    tmp=to_analyse[a+1].split(">")
                    tmp=tmp[4].split("<")
                    QiMoChiCangShu_A=tmp[0].replace(",","")
                    continue

                if to_analyse[a].find("持有<span>B</span>股的投资者")>0 or to_analyse[a].find("持有<SPAN>B</SPAN>股的投资者")>0:
                    tmp=to_analyse[a+1].split(">")
                    tmp=tmp[4].split("<")
                    QiMoChiCangShu_B=tmp[0].replace(",","")
                    continue

                if to_analyse[a].find("期间参与交易的投资者数量")>0:
                    tmp=to_analyse[a+1].split(">")
                    tmp=tmp[4].split("<")
                    CanYuJiaoYiShu=tmp[0].replace(",","")
                    continue

                if to_analyse[a].find("交易<span>A</span>股的投资者")>0 or to_analyse[a].find("交易<SPAN>A</SPAN>股的投资者")>0:
                    tmp=to_analyse[a+1].split(">")
                    tmp=tmp[4].split("<")
                    CanYuJiaoYiShu_A=tmp[0].replace(",","")
                    continue

                if to_analyse[a].find("交易<span>B</span>股的投资者")>0 or to_analyse[a].find("交易<SPAN>B</SPAN>股的投资者")>0:
                    tmp=to_analyse[a+1].split(">")
                    tmp=tmp[4].split("<")
                    CanYuJiaoYiShu_B=tmp[0].replace(",","")
                    continue

            print >>f,Up_to_date,",",XinZengShu,",",XinZengShu_ZiRanRen,",",XinZengShu_Fei_ZiRanRen,",",\
            QiMoShu,",",QiMoShu_ZiRanRen,",",QiMoShu_ZiRanRen_A,",",QiMoShu_ZiRanRen_B,",",QiMoShu_Fei_ZiRanRen,",",QiMoShu_Fei_ZiRanRen_A,",",QiMoShu_Fei_ZiRanRen_B,",",\
            QiMoChiCangShu,",",QiMoChiCangShu_A,",",QiMoChiCangShu_B,",",\
            CanYuJiaoYiShu,",",CanYuJiaoYiShu_A,",",CanYuJiaoYiShu_B

    tmp_date=tmp_date+datetime.timedelta(days=7)
