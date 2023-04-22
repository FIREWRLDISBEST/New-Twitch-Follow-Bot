import httpx, json, time, threading




class Tools:

    def user_id(self, user):
        headers = {'Connection': 'keep-alive','Pragma': 'no-cache','Cache-Control': 'no-cache','sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"','Accept-Language': 'en-US','sec-ch-ua-mobile': '?0','Client-Version': '7b9843d8-1916-4c86-aeb3-7850e2896464','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36','Content-Type': 'text/plain;charset=UTF-8','Client-Session-Id': '51789c1a5bf92c65','Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko','X-Device-Id': 'xH9DusxeZ5JEV7wvmL8ODHLkDcg08Hgr','sec-ch-ua-platform': '"Windows"','Accept': '*/*','Origin': 'https://www.twitch.tv','Sec-Fetch-Site': 'same-site','Sec-Fetch-Mode': 'cors','Sec-Fetch-Dest': 'empty','Referer': 'https://www.twitch.tv/',}
        data = '[{"operationName": "WatchTrackQuery","variables": {"channelLogin": "'+user+'","videoID": null,"hasVideoID": false},"extensions": {"persistedQuery": {"version": 1,"sha256Hash": "38bbbbd9ae2e0150f335e208b05cf09978e542b464a78c2d4952673cd02ea42b"}}}]'
        try:
            response = httpx.post('https://gql.twitch.tv/gql', headers=headers, data=data)
            return response.json()[0]['data']['user']['id']
        except:
            return False


class Follow:

    def send_follow(self, target_id, follow_count, tokens_data):

        class Threads():
                tha = 0
        
        def follow(i):
            Threads.tha = Threads.tha + 1
            try:
                data = json.loads(tokens_data[i])
                Authorization = data['Authorization']
                Integrity = data['Integrity']
                proxy = "http://" + data['proxy']
                X_Device_Id = data['X-Device-Id']
                Client_Id = data['Client-Id']
                User_Agent = data['User-Agent']
                Integrity = data['Integrity']
                Accept_Language = data['Accept-Language']


                payload = '[{"operationName":"FollowButton_FollowUser","variables":{"input":{"disableNotifications":false,"targetID":"'+str(target_id)+'"}},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"800e7346bdf7e5278a3c1d3f21b2b56e2639928f86815677a7126b093b2fdd08"}}}]'
                headers = {
                    
                    'Accept-Language': Accept_Language,
                    'Authorization': 'OAuth '+Authorization,
                    'Client-Id': Client_Id,
                    'Client-Integrity': Integrity,
                    'User-Agent': User_Agent,
                    'X-Device-Id': X_Device_Id,


                    }
                res = httpx.post('https://gql.twitch.tv/gql', data=payload, headers=headers,proxies=proxy,timeout=40)
                print(res.text)
            except:
                pass

            Threads.tha = Threads.tha - 1

        def start():
            for i in range(follow_count):
                while True:
                    time.sleep(0.01)
                    if Threads.tha < 20:
                        threading.Thread(
                            target=follow, args=(i,)).start()
                        break
                    else:
                        time.sleep(1)

        threading.Thread(target=start).start()






