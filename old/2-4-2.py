import discord , asyncio , datetime , sys , os
from web3 import *

def main():
    client = discord.Client()

    #명령어 목록
    Command_list = discord.Embed(title="Command List", description="명령어 목록", color=0x00ff00)
    Command_list.add_field(name="$a", value="도움말", inline=False)
    Command_list.add_field(name="$b", value="버전 정보", inline=False)
    Command_list.add_field(name="$d", value="오늘 날짜", inline=False)
    Command_list.add_field(name="$f", value="내일급식", inline=False)
    Command_list.add_field(name="$g", value="급식정보", inline=False)

    #급식안내
    meal_notice = (
                    "```css\n"
                    "[-] 2018년 1월 2일 인 경우 18012 로 보낼 것.\n"
                    "[-] 2018년 10월 1일 인 경우 18101 로 보낼 것.\n"
                    "```"
                    )

    @client.event
    async def on_member_join(member):
        fmt = ' {1.name} 에 오신걸 환영합니다, {0.mention} 님'
        channel = member.server.get_channel("429208403118653440")
        await client.send_message(channel, fmt.format(member, member.server))
        await client.send_message(member, "공지 읽어주세요")

    @client.event
    async def on_member_remove(member):
        channel = member.server.get_channel("429208403118653440")
        fmt = '{0.mention} 님이 서버에서 나가셨습니다.'
        await client.send_message(channel, fmt.format(member, member.server))

    @client.event
    async def on_ready():
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('---------')
        await client.change_presence(game=discord.Game(name="$a for help"))

    @client.event
    async def on_message(message):
        #함수안에 함수정의
        #---print_get_meal func start---
        async def print_get_meal(local_date, local_weekday):
            l_diet = get_diet(2, local_date, local_weekday)
            d_diet = get_diet(3, local_date, local_weekday)

            if len(l_diet) == 1:
                embed = discord.Embed(title="No Meal", description="급식이 없습니다.", color=0x00ff00)
                await client.send_message(message.channel, embed=embed)
            elif len(d_diet) == 1:
                lunch = local_date + " 중식\n" + l_diet
                embed = discord.Embed(title="Lunch", description=lunch, color=0x00ff00)
                await client.send_message(message.channel, embed=embed)
            else:
                lunch = local_date + " 중식\n" + l_diet
                dinner = local_date + " 석식\n" + d_diet
                lunch_e= discord.Embed(title="Lunch", description=lunch, color=0x00ff00)
                await client.send_message(message.channel, embed=lunch_e)
                dinner_e = discord.Embed(title="Dinner", description=dinner, color=0x00ff00)
                await client.send_message(message.channel, embed=dinner_e)
        #---print_get_meal func end---

        if message.content.startswith('$a'):
            await client.send_message(message.channel, embed=Command_list)

        elif message.content.startswith('$b'):
            embed = discord.Embed(title="Bot Version", description="updated", color=0x00ff00)
            embed.add_field(name="Version", value="2.4.2", inline=False)
            await client.send_message(message.channel, embed=embed)

        elif message.content.startswith('$d'):
            dt = datetime.datetime.now()
            local_time = dt.strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
            embed = discord.Embed(title="Local Time", description=local_time, color=0x00ff00)
            await client.send_message(message.channel, embed=embed)

        elif message.content.startswith('$f'):
            f_dt = datetime.datetime.today() + datetime.timedelta(days=1)
            meal_date = f_dt.strftime("%Y.%m.%d")
            whatday = f_dt.weekday()

            await print_get_meal(meal_date, whatday)

        elif message.content.startswith('$g'):
            request = meal_notice + '\n' + '날짜를 보내주세요...'
            request_e = discord.Embed(title="Send to Me", description=request, color=0xcceeff)
            await client.send_message(message.channel, embed=request_e)
            meal_date = await client.wait_for_message(timeout=15.0, author=message.author)

            if meal_date is None:
                longtimemsg = discord.Embed(title="In 15sec", description='15초내로 입력해주세요. 다시시도 : $g', color=0xff0000)
                await client.send_message(message.channel, embed=longtimemsg)
                return

            else:
                meal_date = str(meal_date.content) # 171121
                meal_date = '20' + meal_date[:2] + '.' + meal_date[2:4] + '.' + meal_date[4:6] # 2017.11.21

                s = meal_date.replace('.', ', ') # 2017, 11, 21

                #한자리수 달인 경우를 해결하기위함
                if int(s[6:8]) < 10:
                    s = s.replace(s[6:8], s[7:8])

                ss = "datetime.datetime(" + s + ").weekday()"
                try:
                    whatday = eval(ss)
                except:
                    warnning = discord.Embed(title="Plz Retry", description='올바른 값으로 다시 시도하세요 : $g', color=0xff0000)
                    await client.send_message(message.channel, embed=warnning)
                    return

                print_get_meal(meal_date, whatday)

    client.run('NDE0NzU0NzM2ODEwNzU0MDY5.DXlfMw.sUeh3BggTGxf_aqBsUhnGB7_2bQ')

    #대기 시간 초과로 봇이 종료되었을 때 자동으로 재실행을 위함
    #import sys, os
    executable = sys.executable
    args = sys.argv[:]
    args.insert(0, sys.executable)
    print("Respawning")
    os.execvp(executable, args)

if __name__ == '__main__':
    main()
