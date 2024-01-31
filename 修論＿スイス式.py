#正規品
import random
import math
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

#変更するパラメータ
kazu = 10000 #試行回数
rounds = 7 #ラウンド数
Meth = 0 #勝敗の決定方法を決める変数（０なら乱数、１なら実力通り、２以降引き分け　２：勝ち２引き分け１　３：勝ち３引き分け１　４：勝ち１引き分け０）
ninzoo = 64 #人数(odds_listを関数によって決める時につかう)
odds_w = 1 #odds_list(0は等差数列、1は正規分布)

#今何回目
nankaime = 0
#転倒数
swistenn = []
soltenn = []
omwtenn = []
solborntenn =[]
MDtenn = []
MDbooktenn = []

#転倒数重み
solteniw = [] 
omwteniw = [] 
sbteniw = [] 
MDteniw = [] 
MDbteniw = []

#かぶり数
solkaburi = [] 
omwkaburi = []
sbkaburi = []
MDkaburi = []
MDbkaburi = []
solsbmdkaburisuu = []
omwsbmdkaburisuu = []
solsbmdbkaburisuu = []

# 同じ勝ち数のプレイヤーだけで計測する転倒数
solten_same_wins = [] 
omwten_same_wins = []
sbten_same_wins = []
MDten_same_wins = []
MDbten_same_wins = []

#top8転倒数について
swis8 = []
sol8 = []
omw8 = []
sb8 = []
Md8 = []
MDb8 = []


#組み合わせのやつ
sol_sb_md = []
sol_md_sb = []
sb_sol_md = []
sb_md_sol = []
md_sol_sb = []
md_sb_sol = []
omw_sb_md = []
omw_md_sb = []
sb_omw_md = []
sb_md_omw = []
md_omw_sb = []
md_sb_omw = []
sol_sb_mdb = []
sol_mdb_sb = []
sb_sol_mdb = []
sb_mdb_sol = []
mdb_sol_sb = []
mdb_sb_sol = []

#組み合わせ勝ち数がラウンド-1転倒数 追記中
sol_sb_md_wn = []
sol_md_sb_wn = []
sb_sol_md_wn = []
sb_md_sol_wn = []
md_sol_sb_wn = []
md_sb_sol_wn = []
omw_sb_md_wn = []
omw_md_sb_wn = []
sb_omw_md_wn = []
sb_md_omw_wn = []
md_omw_sb_wn = []
md_sb_omw_wn = []

solsbt8 = 0
solomwt8 = 0
solmdbt8 = 0
solmdt8 = 0
sbomwt8 = 0
sbmdt8 = 0
sbmdbt8 = 0
omwmdt8 = 0
omwmdbt8 = 0
mdmdbt8 = 0

#playerクラスの定義
class Player:
    def __init__(self, name, odds):
        self.name = name
        #oddsを紐づける
        self.odds = odds
        #プレイヤーの勝ち点を入力
        self.wins = 0
        #プレイヤーの勝ち数を入力
        self.katisuu = 0
        #対戦相手の履歴
        self.match_history = []
        #勝った対戦相手
        self.match_win = []
        #負けた対戦相手
        self.match_WL = []
        #そのプレイヤーの引き分けの回数について
        self.hikiwake = []
        #かぶってるプレイヤーに勝ったら数字が増えていく
        self.donguri = 0
        #omwバージョン
        self.dongooo = 0
        #だれとかぶってるか
        self.kaburiaite = []

#スイストーナメント中身(マッチング方法について改善の余地ありかも)
def swiss_tournament(players, rounds):
    
    # the match history
    for player in players:
        player.match_history = []

    if Meth == 0 or Meth == 1:
        for rnd in range(rounds):
            i = 1
            ni = 0
            while i == 1:

                #Sort players
                players.sort(key=lambda x: (x.wins,random.random()), reverse=True)
                #マッチングが成立しているか確認
                for f in range(0, len(players) - 1, 2):
                    player1 = players[f]
                    player2 = players[f + 1]
                    if player2.name in player1.match_history :
                        i = 1
                        ni = ni+1
                        break
                    else :
                        i = 0
                """
                if ni > 100000:
                    for i, player in enumerate(players):
                        print(f"{i}. {player.name}, Wins: {player.wins}, katisuu: {player.katisuu}")
                        print("Match History:", player.match_history)
                    exit()
                """
            #すべてのマッチングが成立したら、プレイヤーを戦わせる。
            for n in range(0, len(players) - 1, 2):
                player1 = players[n]
                player2 = players[n + 1]
                player1.match_history.append(player2.name)
                player2.match_history.append(player1.name)

                #ランダムで勝ちが決まるシミュレーション
                if Meth == 0:
                    #print("ランダム")
                    if random.random() <= (player1.odds)/(player1.odds + player2.odds):
                        player1.wins += 1
                        player1.match_win.append(player2.name)
                        player2.match_WL.append(player1.name)  
                    else:
                        player2.wins += 1
                        player2.match_win.append(player1.name)
                        player1.match_WL.append(player2.name)
                        

                #実力どおりに勝ちが決まる場合のシミュレーション
                if Meth == 1:
                    #print("実力通り")
                    if player1.odds >= player2.odds:
                        player1.wins += 1
                        player1.match_win.append(player2.name)
                        player2.match_WL.append(player1.name)  
                    else:
                        player2.wins += 1
                        player2.match_win.append(player1.name)
                        player1.match_WL.append(player2.name)  
            
        
    if Meth == 4:
        for rnd in range(rounds):
            i = 1
            o = 0
            while i == 1 :
                for player in players:
                    player.katisuu = player.wins #プレイヤー全員の勝ち数をMethで割って切り捨て、それをplayer.katisuuに埋め込む作業
                
                if o >= 10000:
                    for player in players:
                        if player.katisuu == 0:
                            player.katisuu = 1
                        if rnd == 6:
                            if player.katisuu >=5:
                                player.katisuu = 4

                #Sort players
                players.sort(key=lambda x: (x.katisuu,random.random()), reverse=True)
                #マッチングが成立しているか確認
                for f in range(0, len(players) - 1, 2):
                    player1 = players[f]
                    player2 = players[f + 1]
                    if player2.name in player1.match_history :
                        i = 1
                        o = o + 1
                        break
                    else :
                        i = 0                
                
            #すべてのマッチングが成立したら、プレイヤーを戦わせる。
            for n in range(0, len(players) - 1, 2):
                player1 = players[n]
                player2 = players[n + 1]
                player1.match_history.append(player2.name)
                player2.match_history.append(player1.name)

                #引き分けがあるバージョン（引き分けを勝ち点に含めない場合）
                if Meth == 4:
                    hikiwakeobake = random.random()
                    obake = random.random()
                    if player1.odds >= player2.odds:
                        onakasuita = ((player2.odds / player1.odds) * 0.1 )
                    else:
                        onakasuita = ((player1.odds / player2.odds) * 0.1 )
                    if hikiwakeobake < onakasuita:
                        player1.hikiwake.append(player2.name)
                        player2.hikiwake.append(player1.name)  
                    else:
                        if obake < (player1.odds)/(player1.odds + player2.odds):
                            player1.wins += 1
                            player1.match_win.append(player2.name)
                            player2.match_WL.append(player1.name)  
                        else:
                            player2.wins += 1
                            player2.match_win.append(player1.name)
                            player1.match_WL.append(player2.name)

    if Meth == 2 or Meth == 3:
        for rnd in range(rounds):
            i = 1
            o = 0
            while i == 1 :
                for player in players:
                    player.katisuu = player.wins // Meth#プレイヤー全員の勝ち数をMethで割って切り捨て、それをplayer.katisuuに埋め込む作業
                
                if o >= 1000:
                    for player in players:
                        if player.katisuu == 0:
                            player.katisuu = 1
                        if rnd == 6:
                            if player.katisuu >=5:
                                player.katisuu = 4
                
                #Sort players
                players.sort(key=lambda x: (x.katisuu,random.random()), reverse=True)
                #マッチングが成立しているか確認
                for f in range(0, len(players) - 1, 2):
                    player1 = players[f]
                    player2 = players[f + 1]
                    if player2.name in player1.match_history :
                        i = 1
                        o = o + 1
                        break
                    else :
                        i = 0
                        """
                if o > 10000:
                    for i, player in enumerate(players):
                        print(f"{i}. {player.name}, Wins: {player.wins}, katisuu: {player.katisuu}")
                        print("Match History:", player.match_history)
                    exit()
                        """
    

            #すべてのマッチングが成立したら、プレイヤーを戦わせる。
            for n in range(0, len(players) - 1, 2):
                player1 = players[n]
                player2 = players[n + 1]
                player1.match_history.append(player2.name)
                player2.match_history.append(player1.name)

                #引き分けがある場合のシミュレーション(勝ち点を３、引き分けを１とした場合)
                if Meth == 3:
                    hikiwakeobake = random.random()
                    obake = random.random()
                    if player1.odds >= player2.odds:
                        onakasuita = ((player2.odds / player1.odds) * 0.1 )
                    else:
                        onakasuita = ((player1.odds / player2.odds) * 0.1 )
                    if hikiwakeobake < onakasuita:
                        player1.wins += 1
                        player2.wins += 1
                        player1.hikiwake.append(player2.name)
                        player2.hikiwake.append(player1.name)  
                    else:
                        if obake < (player1.odds)/(player1.odds + player2.odds):
                            player1.wins += 3
                            player1.match_win.append(player2.name)
                            player2.match_WL.append(player1.name)  
                        else:
                            player2.wins += 3
                            player2.match_win.append(player1.name)
                            player1.match_WL.append(player2.name)


                    
                    
                #引き分けがあるバージョン（勝ち点を2、引き分けを1とする場合）
                if Meth == 2:
                    hikiwakeobake = random.random()
                    obake = random.random()
                    if player1.odds >= player2.odds:
                        onakasuita = ((player2.odds / player1.odds) * 0.1 )
                    else:
                        onakasuita = ((player1.odds / player2.odds) * 0.1 )
                    if hikiwakeobake < onakasuita:
                        player1.wins += 1
                        player2.wins += 1
                        player1.hikiwake.append(player2.name)
                        player2.hikiwake.append(player1.name)  
                    else:
                        if obake < (player1.odds)/(player1.odds + player2.odds):
                            player1.wins += 2
                            player1.match_win.append(player2.name)
                            player2.match_WL.append(player1.name)  
                        else:
                            player2.wins += 2
                            player2.match_win.append(player1.name)
                            player1.match_WL.append(player2.name)


    # タイブレイク
    for player in players:
        #タイブレイク計算のためのリスト作成
        #プレイヤーのマッチヒストリーのなかになまえがあるプレイヤーを
        opponents_wins = [p.wins for p in players if player.name in p.match_history]
        oppo_winper = [max(0.25,p.wins/rounds) for p in players if player.name in p.match_history]
        playerww = [p.wins for p in players if player.name in p.match_WL]
        #opponents_winsを昇順で並べ替え
        sort_oppwin = sorted(opponents_wins)


        
        #ソルコフ値計算
        solkoff = sum(opponents_wins) 
        #omw%計算
        omw = round(sum(oppo_winper)/rounds,3)
        #ソルボーンベルガー計算
        solbornberger = sum(playerww)
        #median計算
        median_score = sum(sort_oppwin[1:-1])
        #メディアン・ブックホルツ計算
        if rounds % 2 == 0:
            mid1 = sort_oppwin[int(round(rounds / 2)) - 1]
            mid2 = sort_oppwin[int(round(rounds / 2))]
            median_bookholz = (mid1 + mid2) / 2
        else:
            median_bookholz = sort_oppwin[rounds // 2]

        player.tiebreak_indicators = {
            'Solkoff': solkoff,
            'OMW%': omw,
            'Solbornberger': solbornberger,
            'Median Score': median_score,
            'Median Bookholz': median_bookholz
        }

    return players

#対戦情報
if __name__ == "__main__":
    mawasukaisuu = kazu

    if odds_w == 0:
        odds_list = list(range(ninzoo + 3, 3,-1))
        print(odds_list)
        
    if odds_w == 1:
        odds_list = [2679,2361,2241,2097,2046,2016,2012,1998,1993,1966,1918,1876,1849,1844,1836,1792,1782,1708,1692,1684,1676,1659,1590,1564,1561,1558,1556,1553,1516,1495,1470,1467,1466,1464,1452,1452,1433,1408,1407,1400,1367,1365,1361,1345,1343,1307,1303,1267,1255,1245,1195,1186,1186,1140,1138,1125,1119,1106,1005,961,805,724,631,539]
    print(odds_list)
    aioi = len(odds_list)
    print("a",aioi)
    if odds_w == 2:
        odds_list= []

    for _ in range (mawasukaisuu):

        player_names = [f"Player{i}" for i in range(0, len(odds_list) )]
        players = [Player(name, odds) for name, odds in zip(player_names, odds_list)]

        # go swis tournament
        result_players = swiss_tournament(players, rounds)
        nankaime = nankaime + 1
        print(nankaime)

    #-----------------------------------------------------------------------------------
    #転倒数のターン！！
        def inversion_count(arr):
            count = 0
            for i in range(len(arr)):
                for j in range(i + 1, len(arr)):
                    if arr[i] < arr[j]:
                        count += 1
            return count
        
        

    #転倒数(勝ち数が同じ場合)（本来は勝ち数を取得してそれだけで転倒数獲ればいいんだろうけどやり方がわからないから楽に書きます。）
        """
        def inversion_same_wins(arr,winno):
            count_same_wins = 0
            for i, player1 in enumerate(players):
                print("i",i)
                if player1.wins == winno:
                    print("ih",i)
                    for j, player2 in enumerate(players[i + 1:]):
                        #print("j",j)
                        if player1.wins == player2.wins:
                            if arr[i] < arr[j]:
                                count_same_wins += 1
            return count_same_wins
        """

    #TOP8転倒
        def inversion_top8(arr):
            count8 = 0
            for i in range(8):
                for j in range(8,len(arr)):
                    if arr[i] < arr[j]:
                        count8 += 1

            return count8   
        
    #swisソート(追加部分だよー)
        arr = []

        def swis_sort_key(player):
            return (-player.wins, -player.odds)
        result_players.sort(key=swis_sort_key)

        for i, player in enumerate(result_players, 1):
            arr.append(player.odds)

        swisinv = inversion_count(arr)
        swistenn.append(swisinv)

        swist8 = inversion_top8(arr)
        swis8.append(swist8)

        
        #ソルコフ値順のソート-----------------------------------------------------------
        arr = []
    
        def solcustom_sort_key(player):
            return (-player.wins, -player.tiebreak_indicators['Solkoff'], -player.odds)
        result_players.sort(key=solcustom_sort_key)


        #ソルコフ値並べ替えのオッズの部分(後で検算する)

        for i, player in enumerate(result_players, 1):
            arr.append(player.odds)

        solinv = inversion_count(arr)
        soltenn.append(solinv)

        #top8 sol
        solt8 = inversion_top8(arr)
        sol8.append(solt8)

        #ソルコフ値のかぶり数
        countsol = 0
        for i, player1 in enumerate(players):
            #print("i",i)
            for j , player2 in enumerate(players[i + 1:],start=i + 1):
                #print(j,player2.name)
                if player1.wins == player2.wins and player1.tiebreak_indicators['Solkoff'] == player2.tiebreak_indicators['Solkoff']:
                    countsol = countsol + 1
                    #print(player1.name,player2.name)
        solkaburi.append(countsol)

        



        #omw順のソート----------------------------------------------------------------------
        arr = []
        def omwcustom_sort_key(player):
            return (-player.wins, -player.tiebreak_indicators['OMW%'], -player.odds)
        result_players.sort(key=omwcustom_sort_key)

        #omw並べ替えのオッズの部分
        for i, player in enumerate(result_players, 1):
            arr.append(player.odds)

        omwinv = inversion_count(arr)
        omwtenn.append(omwinv)


        #top8 omw
        omwt8 = inversion_top8(arr)
        omw8.append(omwt8)

        #omwのかぶり数
        countomw = 0
        for i, player1 in enumerate(players):
            #print("i",i)
            for j , player2 in enumerate(players[i + 1:],start=i + 1):
                #print(j,player2.name)
                if player1.wins == player2.wins and player1.tiebreak_indicators['OMW%'] == player2.tiebreak_indicators['OMW%']:
                    countomw = countomw + 1
                    #print(player1.name,player2.name)
        omwkaburi.append(countomw)


        #slb値順のソート---------------------------------------------------------------------
        arr = []
        def slbcustom_sort_key(player):
            return (-player.wins, -player.tiebreak_indicators['Solbornberger'], -player.odds)
        result_players.sort(key=slbcustom_sort_key)

        #slb値並べ替えのオッズの部分
        for i, player in enumerate(result_players, 1):
            arr.append(player.odds)

        slbinv = inversion_count(arr)
        solborntenn.append(slbinv)

        #top8 sb
        sbt8 = inversion_top8(arr)
        sb8.append(sbt8)

        #slbかぶり数
        countslb = 0
        for i, player1 in enumerate(players):
            #print("i",i)
            for j , player2 in enumerate(players[i + 1:],start=i + 1):
                #print(j,player2.name)
                if player1.wins == player2.wins and player1.tiebreak_indicators['Solbornberger'] == player2.tiebreak_indicators['Solbornberger']:
                    countslb = countslb + 1
                    #print(player1.name,player2.name)
        sbkaburi.append(countslb)


        #medi値順のソート----------------------------------------------------------------------
        arr = []
        def medicustom_sort_key(player):
            return (-player.wins, -player.tiebreak_indicators['Median Score'], -player.odds)
        result_players.sort(key=medicustom_sort_key)
        #medi値並べ替えのオッズの部分
        for i, player in enumerate(result_players, 1):
            arr.append(player.odds)

        mediinv = inversion_count(arr)
        MDtenn.append(mediinv)

        Mdt8 = inversion_top8(arr)
        Md8.append(Mdt8)

        #medi値のかぶり
        countMD = 0
        for i, player1 in enumerate(players):
            #print("i",i)
            for j , player2 in enumerate(players[i + 1:],start=i + 1):
                #print(j,player2.name)
                if player1.wins == player2.wins and player1.tiebreak_indicators['Median Score'] == player2.tiebreak_indicators['Median Score']:
                    countMD = countMD + 1
                    #print(player1.name,player2.name)
        MDkaburi.append(countMD)

        #medb値順のソート---------------------------------------------------------------------
        arr = []
        def medbcustom_sort_key(player):
            return (-player.wins, -player.tiebreak_indicators['Median Bookholz'], -player.odds)
        result_players.sort(key=medbcustom_sort_key)

        #medb値並べ替えのオッズの部分
        for i, player in enumerate(result_players, 1):
            arr.append(player.odds)

        medbinv = inversion_count(arr)
        MDbooktenn.append(medbinv)

        #top8 mdb
        mdbt8 = inversion_top8(arr)
        MDb8.append(mdbt8)

        #print(arr,"medbの転倒数は", medbinv)

        #medbかぶり数
        countMDb = 0
        for i, player1 in enumerate(players):
            #print("i",i)
            for j , player2 in enumerate(players[i + 1:],start=i + 1):
                #print(j,player2.name)
                if player1.wins == player2.wins and player1.tiebreak_indicators['Median Bookholz'] == player2.tiebreak_indicators['Median Bookholz']:
                    countMDb = countMDb + 1
                    #print(player1.name,player2.name)
        MDbkaburi.append(countMDb)

        #top8数値が同じこと多くね？
        if solt8 == sbt8:
            solsbt8 = solsbt8 + 1
        if solt8 == omwt8:
            solomwt8 = solomwt8 + 1
        if solt8 == Mdt8:
            solmdt8 = solmdt8 + 1
        if solt8 == mdbt8:
            solmdbt8 = solmdbt8 + 1

        if sbt8 == omwt8:
            sbomwt8 = sbomwt8 + 1
        if sbt8 == Mdt8:
            sbmdt8 = sbmdt8 + 1
        if sbt8 == mdbt8:
            sbmdbt8 = sbmdbt8 + 1

        if omwt8 == Mdt8:
            omwmdt8 = omwmdt8 + 1
        if omwt8 == mdbt8:
            omwmdbt8 = omwmdbt8 + 1

        if Mdt8 == mdbt8:
            mdmdbt8 = mdmdbt8 + 1        

        #ソートを工夫する。
        #コピペ用　-player.tiebreak_indicators['Solkoff']　-player.wins, -player.tiebreak_indicators['Solbornberger']　 -player.tiebreak_indicators['Median Bookholz']

        #かぶる数 sol sb md 三人同じみたいな場合にぶち当たったら超絶だるいことになるかもしれないのだ
        solsbmdkaburi = 0
        for i, player1 in enumerate(players):
            for j , player2 in enumerate(players[i + 1:],start = i + 1):
                if player1.wins == player2.wins and player1.tiebreak_indicators['Solkoff'] == player2.tiebreak_indicators['Solkoff'] and player1.tiebreak_indicators['Solbornberger'] == player2.tiebreak_indicators['Solbornberger'] and player1.tiebreak_indicators['Median Score'] == player2.tiebreak_indicators['Median Score']:
                    if player1.name in player2.match_win:
                        player2.donguri = player2.donguri + 1
                    if player2.name in player1.match_win:
                        player1.donguri = player1.donguri + 1
                    if not player1.name in player2.match_history:
                        solsbmdkaburi = solsbmdkaburi + 1
                        player1.kaburiaite.append(player2.name)
                        player2.kaburiaite.append(player1.name)

        solsbmdkaburisuu.append(solsbmdkaburi) 
        
        #sol sb md
        arr = []
        def sol_sb_md_sort_key(player):
            return (-player.wins, -player.tiebreak_indicators['Solkoff'], -player.tiebreak_indicators['Solbornberger'], -player.tiebreak_indicators['Median Score'],-player.donguri,-player.odds)
        result_players.sort(key=sol_sb_md_sort_key)

        for i, player in enumerate(result_players, 1):
            arr.append(player.odds)

        solsbmdinv = inversion_count(arr)
        sol_sb_md.append(solsbmdinv)
    
        #sol md sb
        arr = []
        def sol_md_sb_sort_key(player):
            return (-player.wins, -player.tiebreak_indicators['Solkoff'], -player.tiebreak_indicators['Median Score'], -player.tiebreak_indicators['Solbornberger'],-player.donguri,-player.odds)
        result_players.sort(key=sol_md_sb_sort_key)

        for i, player in enumerate(result_players, 1):
            arr.append(player.odds)

        solmdsbinv = inversion_count(arr)
        sol_md_sb.append(solmdsbinv)
        
        #sb sol md
        arr = []
        def sb_sol_md_sort_key(player):
            return (-player.wins, -player.tiebreak_indicators['Solbornberger'], -player.tiebreak_indicators['Solkoff'], -player.tiebreak_indicators['Median Score'],-player.donguri,-player.odds)
        result_players.sort(key=sb_sol_md_sort_key)

        for i, player in enumerate(result_players, 1):
            arr.append(player.odds)

        sbsolmdinv = inversion_count(arr)
        sb_sol_md.append(sbsolmdinv)
       
        #sb md sol
        arr = []
        def sb_md_sol_sort_key(player):
            return (-player.wins, -player.tiebreak_indicators['Solbornberger'], -player.tiebreak_indicators['Median Score'], -player.tiebreak_indicators['Solkoff'],-player.donguri,-player.odds)
        result_players.sort(key=sb_md_sol_sort_key)

        for i, player in enumerate(result_players, 1):
            arr.append(player.odds)
        
        sbmdsolinv = inversion_count(arr)
        sb_md_sol.append(sbmdsolinv)

        #md sol sb
        arr = []
        def md_sol_sb_sort_key(player):
            return (-player.wins, -player.tiebreak_indicators['Median Score'], -player.tiebreak_indicators['Solkoff'], -player.tiebreak_indicators['Solbornberger'],-player.donguri,-player.odds)
        result_players.sort(key=md_sol_sb_sort_key)

        for i, player in enumerate(result_players, 1):
            arr.append(player.odds)

        mdsolsbinv = inversion_count(arr)
        md_sol_sb.append(mdsolsbinv)
       
        #md sb sol
        arr = []
        def md_sb_sol_sort_key(player):
            return (-player.wins, -player.tiebreak_indicators['Median Score'], -player.tiebreak_indicators['Solbornberger'], -player.tiebreak_indicators['Solkoff'],-player.donguri,-player.odds)
        result_players.sort(key=md_sb_sol_sort_key)

        for i, player in enumerate(result_players, 1):
            arr.append(player.odds)
       
        mdsbsolinv = inversion_count(arr)
        md_sb_sol.append(mdsbsolinv)

        #omwに変換してみた
        omwsbmdkaburi = 0
        for i, player1 in enumerate(players):
            for j , player2 in enumerate(players[i + 1:],start = i + 1):
                if player1.wins == player2.wins and player1.tiebreak_indicators['OMW%'] == player2.tiebreak_indicators['OMW%'] and player1.tiebreak_indicators['Solbornberger'] == player2.tiebreak_indicators['Solbornberger'] and player1.tiebreak_indicators['Median Score'] == player2.tiebreak_indicators['Median Score']:
                    if player1.name in player2.match_win:
                        player2.dongooo = player2.dongooo + 1
                    if player2.name in player1.match_win:
                        player1.dongooo = player1.dongooo + 1
                    if not player1.name in player2.match_history:
                        omwsbmdkaburi = omwsbmdkaburi + 1
        omwsbmdkaburisuu.append(omwsbmdkaburi)


        #omw% sb md
        arr = []
        def omw_sb_md_sort_key(player):
            return (-player.wins, -player.tiebreak_indicators['OMW%'], -player.tiebreak_indicators['Solbornberger'], -player.tiebreak_indicators['Median Score'],-player.dongooo,-player.odds)
        result_players.sort(key=omw_sb_md_sort_key)

        for i, player in enumerate(result_players, 1):
            arr.append(player.odds)

        omwsbmdinv = inversion_count(arr)
        omw_sb_md.append(omwsbmdinv)

        #omw md sb
        arr = []
        def omw_md_sb_sort_key(player):
            return (-player.wins, -player.tiebreak_indicators['OMW%'], -player.tiebreak_indicators['Median Score'], -player.tiebreak_indicators['Solbornberger'],-player.dongooo,-player.odds)
        result_players.sort(key=omw_md_sb_sort_key)

        for i, player in enumerate(result_players, 1):
            arr.append(player.odds)

        omwmdsbinv = inversion_count(arr)
        omw_md_sb.append(omwmdsbinv)

        #sb omw md
        arr = []
        def sb_omw_md_sort_key(player):
            return (-player.wins, -player.tiebreak_indicators['Solbornberger'], -player.tiebreak_indicators['OMW%'], -player.tiebreak_indicators['Median Score'],-player.dongooo,-player.odds)
        result_players.sort(key=sb_omw_md_sort_key)

        for i, player in enumerate(result_players, 1):
            arr.append(player.odds)

        sbomwmdinv = inversion_count(arr)
        sb_omw_md.append(sbomwmdinv)

        #sb md omw
        arr = []
        def sb_md_omw_sort_key(player):
            return (-player.wins, -player.tiebreak_indicators['Solbornberger'], -player.tiebreak_indicators['Median Score'], -player.tiebreak_indicators['OMW%'],-player.dongooo,-player.odds)
        result_players.sort(key=sb_md_omw_sort_key)

        for i, player in enumerate(result_players, 1):
            arr.append(player.odds)
        
        sbmdomwinv = inversion_count(arr)
        sb_md_omw.append(sbmdomwinv)

        #md omw sb
        arr = []
        def md_omw_sb_sort_key(player):
            return (-player.wins, -player.tiebreak_indicators['Median Score'], -player.tiebreak_indicators['OMW%'], -player.tiebreak_indicators['Solbornberger'] ,-player.dongooo,-player.odds)
        result_players.sort(key=md_omw_sb_sort_key)

        for i, player in enumerate(result_players, 1):
            arr.append(player.odds)

        mdomwsbinv = inversion_count(arr)
        md_omw_sb.append(mdomwsbinv)

        #md sb omw
        arr = []
        def md_sb_omw_sort_key(player):
            return (-player.wins, -player.tiebreak_indicators['Median Score'], -player.tiebreak_indicators['Solbornberger'], -player.tiebreak_indicators['OMW%'],-player.dongooo,-player.odds)
        result_players.sort(key=md_sb_omw_sort_key)

        for i, player in enumerate(result_players, 1):
            arr.append(player.odds)
       
        mdsbomwinv = inversion_count(arr)
        md_sb_omw.append(mdsbomwinv)

                #プリント-------------------------------------------------------------------------------------------
        
        for i, player in enumerate(result_players, 1):
            print(f"{i}. {player.name}, Wins: {player.wins}, odds: {player.odds},Tiebreak : {player.tiebreak_indicators}")
            print("Match History:", player.match_history)
            print("kati",player.match_win)
            print("hikiwake",player.hikiwake)
            #print("kaburi",player.kaburiaite)
            #print("donguri",player.donguri,"dongoo", player.dongooo)
        
        #かぶる数 sol sb mdb
        solsbmdbkaburi = 0
        for i, player1 in enumerate(players):
            for j , player2 in enumerate(players[i + 1:],start = i + 1):
                if player1.wins == player2.wins and player1.tiebreak_indicators['Solkoff'] == player2.tiebreak_indicators['Solkoff'] and player1.tiebreak_indicators['Solbornberger'] == player2.tiebreak_indicators['Solbornberger'] and player1.tiebreak_indicators['Median Bookholz'] == player2.tiebreak_indicators['Median Bookholz']:
                    if player1.name in player2.match_win:
                        player2.donguri = player2.donguri + 1
                    if player2.name in player1.match_win:
                        player1.donguri = player1.donguri + 1
                    if not player1.name in player2.match_history:
                        solsbmdbkaburi = solsbmdbkaburi + 1
                        player1.kaburiaite.append(player2.name)
                        player2.kaburiaite.append(player1.name)

        solsbmdbkaburisuu.append(solsbmdbkaburi) 
        
        #sol sb mdb
        arr = []
        def sol_sb_mdb_sort_key(player):
            return (-player.wins, -player.tiebreak_indicators['Solkoff'], -player.tiebreak_indicators['Solbornberger'], -player.tiebreak_indicators['Median Bookholz'],-player.donguri,-player.odds)
        result_players.sort(key=sol_sb_mdb_sort_key)

        for i, player in enumerate(result_players, 1):
            arr.append(player.odds)

        solsbmdbinv = inversion_count(arr)
        sol_sb_mdb.append(solsbmdbinv)
    
        #sol mdb sb
        arr = []
        def sol_mdb_sb_sort_key(player):
            return (-player.wins, -player.tiebreak_indicators['Solkoff'], -player.tiebreak_indicators['Median Bookholz'], -player.tiebreak_indicators['Solbornberger'],-player.donguri,-player.odds)
        result_players.sort(key=sol_mdb_sb_sort_key)

        for i, player in enumerate(result_players, 1):
            arr.append(player.odds)

        solmdbsbinv = inversion_count(arr)
        sol_mdb_sb.append(solmdbsbinv)
        
        #sb sol mdb
        arr = []
        def sb_sol_mdb_sort_key(player):
            return (-player.wins, -player.tiebreak_indicators['Solbornberger'], -player.tiebreak_indicators['Solkoff'], -player.tiebreak_indicators['Median Bookholz'],-player.donguri,-player.odds)
        result_players.sort(key=sb_sol_mdb_sort_key)

        for i, player in enumerate(result_players, 1):
            arr.append(player.odds)

        sbsolmdbinv = inversion_count(arr)
        sb_sol_mdb.append(sbsolmdbinv)
       
        #sb mdb sol
        arr = []
        def sb_mdb_sol_sort_key(player):
            return (-player.wins, -player.tiebreak_indicators['Solbornberger'], -player.tiebreak_indicators['Median Bookholz'], -player.tiebreak_indicators['Solkoff'],-player.donguri,-player.odds)
        result_players.sort(key=sb_mdb_sol_sort_key)

        for i, player in enumerate(result_players, 1):
            arr.append(player.odds)
        
        sbmdbsolinv = inversion_count(arr)
        sb_mdb_sol.append(sbmdbsolinv)

        #mdb sol sb
        arr = []
        def mdb_sol_sb_sort_key(player):
            return (-player.wins, -player.tiebreak_indicators['Median Bookholz'], -player.tiebreak_indicators['Solkoff'], -player.tiebreak_indicators['Solbornberger'],-player.donguri,-player.odds)
        result_players.sort(key=mdb_sol_sb_sort_key)

        for i, player in enumerate(result_players, 1):
            arr.append(player.odds)

        mdbsolsbinv = inversion_count(arr)
        mdb_sol_sb.append(mdbsolsbinv)
       
        #mdb sb sol
        arr = []
        def mdb_sb_sol_sort_key(player):
            return (-player.wins, -player.tiebreak_indicators['Median Bookholz'], -player.tiebreak_indicators['Solbornberger'], -player.tiebreak_indicators['Solkoff'],-player.donguri,-player.odds)
        result_players.sort(key=mdb_sb_sol_sort_key)

        for i, player in enumerate(result_players, 1):
            arr.append(player.odds)
       
        mdbsbsolinv = inversion_count(arr)
        mdb_sb_sol.append(mdbsbsolinv)


        

#標準偏差用
def standard_deviation(data):
    n = len(data)
    if n == 0:
        return 0
    mean = sum(data) / n
    variance = sum((x - mean) ** 2 for x in data) / n
    return math.sqrt(variance)

'''
#相関係数計算用
corsol, sol_p_value = stats.pearsonr(soltenn, solkaburi)
coromw, omw_p_value = stats.pearsonr(omwtenn, omwkaburi)
corslb, slb_p_value = stats.pearsonr(solborntenn, sbkaburi)
corMD, MD_p_value = stats.pearsonr(MDtenn, MDkaburi)
corMDb, MDb_p_value = stats.pearsonr(MDbooktenn, MDbkaburi)
'''

#タイブレイクしよう前と使用後の差異を出すよ(なんかつぎ足しすぎていびつなコードになっている気がする；；)
solsai = []
omwsai = []
slbsai = []
MDsai = []
MDbsai = []
for i in range(kazu):
    solsa = soltenn[i] - swistenn[i]
    solsai.append(solsa)
    omwsa = omwtenn[i] - swistenn[i]
    omwsai.append(omwsa)
    slbsa = solborntenn[i] - swistenn[i]
    slbsai.append(slbsa)
    MDsa = MDtenn[i] - swistenn[i]
    MDsai.append(MDsa)
    MDbsa = MDbooktenn[i] - swistenn[i]
    MDbsai.append(MDbsa)

#top8も差異を出すよ！
sol8sai = []
omw8sai = []
slb8sai = []
MD8sai = []
MDb8sai = []
for i in range(kazu):
    sol8sa = sol8[i] - swis8[i]
    sol8sai.append(sol8sa)
    omw8sa = omw8[i] - swis8[i]
    omw8sai.append(omw8sa)
    slbsa = sb8[i] - swis8[i]
    slb8sai.append(slbsa)
    Md8sa = Md8[i] - swis8[i]
    MD8sai.append(Md8sa)
    MDb8sa = MDb8[i] - swis8[i]
    MDb8sai.append(MDb8sa)


'''
print(soltenn,
      omwtenn,
      solborntenn,
      MDtenn,
      MDbooktenn)
'''
print("差異込み転倒数",
      sum(solsai)/mawasukaisuu,
      sum(omwsai)/mawasukaisuu,
      sum(slbsai)/mawasukaisuu,
      sum(MDsai)/mawasukaisuu,
      sum(MDbsai)/mawasukaisuu)

print("Top8差異込み転倒数は",
      sum(sol8sai)/mawasukaisuu,
      sum(omw8sai)/mawasukaisuu,
      sum(slb8sai)/mawasukaisuu,
      sum(MD8sai)/mawasukaisuu,
      sum(MDb8sai)/mawasukaisuu)

print("転倒数の平均は",
      sum(soltenn)/mawasukaisuu,
      sum(omwtenn)/mawasukaisuu,
      sum(solborntenn)/mawasukaisuu,
      sum(MDtenn)/mawasukaisuu,
      sum(MDbooktenn)/mawasukaisuu)

print("スイスドロー転倒数",sum(swistenn)/mawasukaisuu)


print("top8とその他の転倒数の平均は",
      sum(sol8)/mawasukaisuu,
      sum(omw8)/mawasukaisuu,
      sum(sb8)/mawasukaisuu,
      sum(Md8)/mawasukaisuu,
      sum(MDb8)/mawasukaisuu      
      )

print("swistop8",sum(swis8)/mawasukaisuu)

print("転倒数の標準偏差は",
      standard_deviation(soltenn),
      standard_deviation(omwtenn),
      standard_deviation(solborntenn),
      standard_deviation(MDtenn),
      standard_deviation(MDbooktenn))

print("勝ち数ごとの転倒数は")


#二乗和っぽくなっているので要検討
print("かぶりの平均は",
      sum(solkaburi)/(mawasukaisuu ),
      sum(omwkaburi)/(mawasukaisuu ),
      sum(sbkaburi)/(mawasukaisuu ),
      sum(MDkaburi)/(mawasukaisuu ),
      sum(MDbkaburi)/(mawasukaisuu ),
      "solsbmd",
      sum(solsbmdkaburisuu)/(mawasukaisuu ),
      "omwsbmd",
      sum(omwsbmdkaburisuu)/(mawasukaisuu ),
      "solsbmdb",
      sum(solsbmdbkaburisuu)/(mawasukaisuu )
      )

#勝ち数ごとの転倒数の実装

#転倒数組み合わせ
print("転倒数組み合わせ",
      "sol",
      sum(sol_sb_md)/mawasukaisuu,
      sum(sol_md_sb)/mawasukaisuu,
      sum(sb_sol_md)/mawasukaisuu,
      sum(sb_md_sol)/mawasukaisuu,
      sum(md_sol_sb)/mawasukaisuu,
      sum(md_sb_sol)/mawasukaisuu,
      "omw",
      sum(omw_sb_md)/mawasukaisuu,
      sum(omw_md_sb)/mawasukaisuu,
      sum(sb_omw_md)/mawasukaisuu,
      sum(sb_md_omw)/mawasukaisuu,
      sum(md_omw_sb)/mawasukaisuu,
      sum(md_sb_omw)/mawasukaisuu,
      "mdb",
      sum(sol_sb_mdb)/mawasukaisuu,
      sum(sol_mdb_sb)/mawasukaisuu,
      sum(sb_sol_mdb)/mawasukaisuu,
      sum(sb_mdb_sol)/mawasukaisuu,
      sum(mdb_sol_sb)/mawasukaisuu,
      sum(mdb_sb_sol)/mawasukaisuu)

print(solsbt8,solomwt8,solmdbt8,solmdt8,sbomwt8,sbmdt8,sbmdbt8,omwmdt8 ,omwmdbt8,mdmdbt8)