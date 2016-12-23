# coding=utf-8


import urllib
#from datetime import datetime
import datetime
import time
import pandas as pd


def Analysis_Var_2_display_in_html(*x):
    #stock_name（哪个股票）,merge_filepath（从哪个文件读取）,date_from_which_year（取哪个时间段的数据），X_column（X轴在哪列取数），Y1_column(Y1在哪列取数)，Y2_column(Y2在哪列取数)... ...
    stock_name=x[0]
    merge_filepath=x[1]
    date_from_which_year=x[2]


    df_temp=pd.read_csv(merge_filepath)
    df_temp.index=pd.tseries.index.DatetimeIndex(df_temp.ix[:,0])
    title_str='\''+stock_name+' Latest Date:'+df_temp.tail(1).ix[:,0].max()+'\''


    x_column=x[3]
    Date_X_axis=list(df_temp[df_temp.index>datetime.datetime(date_from_which_year,1,1)].ix[:,x_column])
    columns_len=len(df_temp.columns)

    Y1_column=x[4]
    Y1_name=df_temp.columns[Y1_column]
    df_temp_2=df_temp.ix[:,Y1_column]
    df_temp_2[df_temp_2.isnull()==True]=' '
    Y1_Value=str(list(df_temp_2[df_temp_2.index>datetime.datetime(date_from_which_year,1,1)]))
    Y1_Value=Y1_Value.replace('\'','')

    #格式变成了2016涨幅，2016涨幅Z分数，2015涨幅，2015涨幅Z分数，2014涨幅，2014涨幅Z分数，
    Y2_column=x[5]
    Y2_name=df_temp.columns[Y2_column]
    df_temp_2=df_temp.ix[:,Y2_column]
    df_temp_2[df_temp_2.isnull()==True]=' '
    Y2_Value=str(list(df_temp_2[df_temp_2.index>datetime.datetime(date_from_which_year,1,1)]))
    Y2_Value=Y2_Value.replace('\'','')

    Y3_column=x[6]
    Y3_name=df_temp.columns[Y3_column]
    df_temp_2=df_temp.ix[:,Y3_column]
    df_temp_2[df_temp_2.isnull()==True]=' '
    Y3_Value=str(list(df_temp_2[df_temp_2.index>datetime.datetime(date_from_which_year,1,1)]))
    Y3_Value=Y3_Value.replace('\'','')

    return title_str,Date_X_axis,Y1_name,Y1_Value,Y2_name,Y2_Value,Y3_name,Y3_Value

#改进后一个页面可以有多个窗口展示
def Write_2_html_with_picture_num(*x):
    global last_write_2_html_filepath
    #(写入文件名,标题,X横坐标,Y1变量名，Y1变量值，Y2变量名，Y2变量值......   ）
    #用以区分

    #写入内容到html的文件路径
    write_2_html_filepath=x[0]
    if last_write_2_html_filepath!=write_2_html_filepath:
        f=open(write_2_html_filepath,'w')
    else:
        f=open(write_2_html_filepath,'a')

    write_2_html_part_1_session_0_0="""
    <!DOCTYPE html>
    <head>
        <meta charset="utf-8">
    """

#    write_2_html_part_1_session_1="""
#    </head>
#    <body>
#        <div id="main" style="height:700px"></div>
#        <script src="http://echarts.baidu.com/build/dist/echarts.js"></script>
#        <script type="text/javascript">
#    """

    write_2_html_part_1_session_0_1="""
    </head>"""

#改进后一个页面可以有多个窗口展示
    write_2_html_part_1_session_1_0="""
    <body>
    """
    write_2_html_part_1_session_1_1="""
        <script src="http://echarts.baidu.com/build/dist/echarts.js"></script>
        <script type="text/javascript">
    """

     #标题
    title_str=x[1]

    #以title_str字符串作为图表窗口命名，但是要去掉单引号'
    chart_windows_name=title_str.replace("'","")

    #因为需要在一个html文件中展示多个图表，必须确保头部文件只打印一次
    if last_write_2_html_filepath!=write_2_html_filepath:
        print >>f,write_2_html_part_1_session_0_0
        print >>f,"<title>",title_str,"</title>"
        print >>f,write_2_html_part_1_session_0_1
        last_write_2_html_filepath=write_2_html_filepath

    print >>f,write_2_html_part_1_session_1_0
    #title_str就作为html展现的窗口代号
    print >>f,"<div id=\"",chart_windows_name,"\" style=\"height:700px\"></div>"
    print >>f,write_2_html_part_1_session_1_1

    #横坐标:日期
    Date_A = x[2]
    xAxis_last_day=Date_A[-1]

    print >>f,'Date_A=',Date_A
    print >>f,'Latest_Date=',title_str
    print >>f,'\n'

    #有多少Y变量?
    Y_var_number=(len(x)-3)/2

    Z_Score_tag=0
    #输出变量名称
    for i in range(0,Y_var_number):
        print >>f,'var_%s'%i,'=','\'',x[3+2*i+1-1],'\''
        if "Z_Score" in x[3+2*i+1-1]:
            Z_Score_tag=1

    print >>f,'\n'

    #列数不要跟输出的xls文件相混淆了，这里取的是程序中的变量数值
    #这里的Data_All是告诉总共有多少Y变量，后续将用到
    Data_All='['
    for i in range(0,Y_var_number):
        Data_All=Data_All+'var_'+str(i)+','
        if i==int(Y_var_number/2)-1:
            Data_All=Data_All+'\'\','

    Data_All=Data_All+']'

    #输出变量值
    for i in range(0,Y_var_number):
        print >>f,'data_%s'%i,'=',x[3+2*i+2-1]

    print >>f,'\n'

    write_2_html_part_3_0="""
        require.config({
            paths: {
                echarts: 'http://echarts.baidu.com/build/dist'
            }
        });

        require(
            [
                'echarts',
                'echarts/chart/line'
            ],
            function (ec) {
    """

    write_2_html_part_3_1="""
                var option = {
    tooltip : {
        trigger: 'axis'
    },
    title : {
        text: Latest_Date,
    """
    print >>f,write_2_html_part_3_0
    #title_str就作为html展现的窗口代号
    print >>f,"var myChart = ec.init(document.getElementById('",chart_windows_name,"'));"
    print >>f,write_2_html_part_3_1


    write_2_html_part_3_modify="""
        x   : 'center',
        y   : 'bottom',
    },
    legend: {
    """

    print >>f,write_2_html_part_3_modify

    print >>f,' data:',Data_All

    write_2_html_part_5="""
        },
        toolbox: {
            show : true,
               x : 'right',
               y : 'center',
          orient : 'vertical',
            feature : {
                mark : {show: true},
                dataView : {show: true, readOnly: false},
                magicType : {show: true, type: ['line', 'bar', 'stack', 'tiled']},
                restore : {show: true},
                saveAsImage : {show: true}
            }
        },
        dataZoom : {
        show : true,
        realtime: true,
        start : 0,
        end : 100
        },
        calculable : true,
        xAxis : [
            {
                type : 'category',
                boundaryGap : false,
                  data : Date_A
            }
        ],
        yAxis : [
            {
                type : 'value'
            }
        ],
        series : [
    """
    print >>f,write_2_html_part_5

    for i in range(0,Y_var_number):
        if i==0 and Z_Score_tag==1:
            print >>f,'        {'
            print >>f,'            name:var_%s,'%i
            print >>f,'            type:\'line\','
            print >>f,'            tiled: \'USD\','
            print >>f,'            data:data_%s,'%i
            print >>f,'            markLine:{'
            print >>f,'                      data:['
            print >>f,'                             [{name: \'Z_Score=1 Start\', value:1,xAxis: 0, yAxis: 1},{name: \'Z_Score=1 End\', xAxis:\'%s\',yAxis: 1}],'%xAxis_last_day
            print >>f,'                             [{name: \'Z_Score=-1 Start\',  value:-1,xAxis: 0, yAxis: -1},{name: \'Z_Score=-1 End\', xAxis:\'%s\',yAxis: -1}]'%xAxis_last_day
            print >>f,'                           ],'
            print >>f,'                      }'
            print >>f,'        },'
        else:
            print >>f,'        {'
            print >>f,'            name:var_%s,'%i
            print >>f,'            type:\'line\','
            print >>f,'            tiled: \'USD\','
            print >>f,'            data:data_%s'%i
            print >>f,'        },'


    write_2_html_part_7="""
        ]
    };

                    myChart.setOption(option);
                }
            );
        </script>
    </body>
    """
    print >>f,write_2_html_part_7
    f.close()


last_write_2_html_filepath=""

#2015年5月8日这是系统上最早能查到的数据
start_date=datetime.date(2015,5,8)
now_date = datetime.datetime.now().date()


local_date_4_file=time.strftime('%Y%m%d',time.localtime(time.time()-24*60*60))
out_file="c:\\IBM-9\\ChinaClear4Customer"+"_"+local_date_4_file+".csv"
write_2_html_filepath="c:\\IBM-9\\ChinaClear4Customer"+"_"+local_date_4_file+".html"

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

f.close()

date_from_which_year=2014
title_str,Date_X_axis,Y1_name,Y1_Value,Y2_name,Y2_Value,Y3_name,Y3_Value=Analysis_Var_2_display_in_html('中国清算_新增投资者数',out_file,date_from_which_year,0,1,2,3)
Write_2_html_with_picture_num(write_2_html_filepath,title_str,Date_X_axis,Y1_name,Y1_Value,Y2_name,Y2_Value,Y3_name,Y3_Value)

date_from_which_year=2014
title_str,Date_X_axis,Y1_name,Y1_Value,Y2_name,Y2_Value,Y3_name,Y3_Value=Analysis_Var_2_display_in_html('投资者数',out_file,date_from_which_year,0,4,5,8)
Write_2_html_with_picture_num(write_2_html_filepath,title_str,Date_X_axis,Y1_name,Y1_Value,Y2_name,Y2_Value,Y3_name,Y3_Value)

date_from_which_year=2014
title_str,Date_X_axis,Y1_name,Y1_Value,Y2_name,Y2_Value,Y3_name,Y3_Value=Analysis_Var_2_display_in_html('持仓的交易者数',out_file,date_from_which_year,0,11,12,13)
Write_2_html_with_picture_num(write_2_html_filepath,title_str,Date_X_axis,Y1_name,Y1_Value,Y2_name,Y2_Value,Y3_name,Y3_Value)

date_from_which_year=2014
title_str,Date_X_axis,Y1_name,Y1_Value,Y2_name,Y2_Value,Y3_name,Y3_Value=Analysis_Var_2_display_in_html('参与交易的交易者数',out_file,date_from_which_year,0,14,15,16)
Write_2_html_with_picture_num(write_2_html_filepath,title_str,Date_X_axis,Y1_name,Y1_Value,Y2_name,Y2_Value,Y3_name,Y3_Value)
