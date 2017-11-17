import discord
import asyncio
import datetime
from web3 import *

client = discord.Client()

#명령어 목록
Command_list = (
                "```css\n"
                "$help : '도움말'\n"
                "$V : '버전 정보'\n"
                "$안녕 : '안녕'\n"
                "$t : '오늘 날짜'\n"
                "$report : '버그 제보하기'\n"
                "$g : '급식정보'\n"
                "```"
                )

#급식안내
meal_notice = (
                "```css\n"
                "[안내] 날짜와 급식이 맞지 않는 경우 개발자에게 문의해주세요.\n"
                "[주의] 2017년 11월 17일 인 경우 17.11.18 로 보낼 것.\n"
                "```"
                )

plus_meal_notice = ""

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('---------')

@client.event
async def on_message(message):
    #시간
    dt = datetime.datetime.now()
    local_date = dt.strftime("%Y년 %m월 %d일 %H시 %M분 %S초")

    if message.content.startswith('$help'):
        await client.send_message(message.channel, Command_list)

    elif message.content.startswith('$V'):
        await client.send_message(message.channel, "버전 : 2.0.0")

    elif message.content.startswith('$안녕'):
        await client.send_message(message.channel, "안녕")

    elif message.content.startswith('$t'):
        await client.send_message(message.channel, local_date)

    elif message.content.startswith('$report'):
        await client.send_message(message.channel, "관리자에게 메세지를 남길 수 있습니다.\n보내주세요:")
        leave_msg = await client.wait_for_message(author=message.author)
        print(local_date)
        print(message.author)
        print(str(leave_msg.content))
        print('------')
        await client.send_message(message.channel, "성공")

    elif message.content.startswith('$g'):
        await client.send_message(message.channel, meal_notice + '\n' + plus_meal_notice + '날짜를 보내주세요...')
        meal_date = await client.wait_for_message(timeout=10.0, author=message.author)

        if meal_date is None:
            longtimemsg = '10초내로 입력해주세요. 다시시도 : $g'
            await client.send_message(message.channel, longtimemsg)
            return

        else:
            await client.send_message(message.channel, '기다려봐...')
            meal_date = '20' + str(meal_date.content)

            s = meal_date.replace('.', ', ') # 2017, 11, 17
            ss = "datetime.datetime(" + s + ").weekday()"
            whatday = eval(ss)

            l_diet = get_diet(2, meal_date, whatday)
            d_diet = get_diet(3, meal_date, whatday)

            if len(l_diet) == 1:
                l_diet = "급식이 없습니다."
                await client.send_message(message.channel, l_diet)
            else:
                lunch = meal_date + " 중식\n" + l_diet
                dinner = meal_date + " 석식\n" + d_diet
                await client.send_message(message.channel, lunch)
                await client.send_message(message.channel, dinner)

client.run('Mzc0MDk0MTc1MDYwMDk5MDc1.DNdYdg.KIvtNwxsdRG9vMyteq4Uae8vQ-w')
