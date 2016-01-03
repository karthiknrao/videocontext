import cv2
import cv
import pdb

#url = 'https://redirector.googlevideo.com/videoplayback?expire=1451687506&source=youtube&sparams=dur%2Cid%2Cip%2Cipbits%2Citag%2Clmt%2Cmime%2Crequiressl%2Csource%2Cupn%2Cexpire&signature=CD9092856F3BFD7BCB7501907A2898C85B424184.028027773110BD984DD7EE70D8D0F8188507A50A&ipbits=0&upn=_PqCZDMGEMI&mime=video%2F3gpp&fexp=9408938%2C9416126%2C9416402%2C9417223%2C9420016%2C9420452%2C9422541%2C9422596%2C9423662%2C9423857%2C9424217%2C9425670%2C9426411%2C9426498&key=yt6&lmt=1451451915833386&ip=115.118.104.11&dur=612.913&id=2538eff6038e16d9&sver=3&itag=36&requiressl=yes&ratebypass=yes'
#url = 'https://r15---sn-cvh7zn7r.googlevideo.com/videoplayback?initcwndbps=130000&sver=3&ipbits=0&dur=72.492&expire=1451688237&ip=115.118.104.11&requiressl=yes&ms=au&mt=1451666570&sparams=cwbhb%2Cdur%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cnh%2Cpl%2Crequiressl%2Csource%2Cupn%2Cexpire&mv=m&id=o-AJx35poicNI29l9rpJ2UVN0tkDuyCumRsls1r4JqiZZv&pl=24&mm=31&mn=sn-cvh7zn7r&fexp=9412776%2C9416126%2C9417224%2C9418203%2C9418223%2C9420452%2C9422596%2C9423411%2C9423662%2C9425954&lmt=1450123246733855&upn=CxeJ5NLnAKU&source=youtube&itag=36&mime=video%2F3gpp&key=yt6&cwbhb=yes&nh=IgpwcjAxLmJvbTAzKgkxMjcuMC4wLjE&signature=CE403442202E175A85F7276FFE9196A2ABC51E39.DB8E8FEDC372673AA11B6E67E87A483C32A97ADA&ratebypass=yes'
#url = 'https://r5---sn-cvh7zn7s.googlevideo.com/videoplayback?upn=bqJZkEF3H0Y&signature=67E184112DE4219476BE0D6104276E299925D7C0.318694CA01FFD958932FB38C6701F2636826A449&sparams=dur%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cnh%2Cpl%2Crequiressl%2Csource%2Cupn%2Cexpire&ipbits=0&nh=IgpwcjAxLmJvbTAzKgkxMjcuMC4wLjE&fexp=9407193%2C9408255%2C9408354%2C9410706%2C9415387%2C9416126%2C9418203%2C9418751%2C9420452%2C9420540%2C9422596%2C9423662%2C9424115%2C9424134%2C9425006%2C9425957&mime=video%2F3gpp&itag=36&pl=24&mv=m&mt=1451666691&ms=au&requiressl=yes&mn=sn-cvh7zn7s&mm=31&initcwndbps=130000&source=youtube&id=o-AD8FgkUkjpnDm_nzsfcRw1iWzMRJK6i-0tBJtwl9rWj3&sver=3&lmt=1450984137656971&ip=115.118.104.11&key=yt6&expire=1451688360&dur=199.505&ratebypass=yes'
url = 'https://r15---sn-cvh7zn7r.googlevideo.com/videoplayback?pl=24&requiressl=yes&expire=1451688696&nh=IgpwcjAxLmJvbTAzKgkxMjcuMC4wLjE&initcwndbps=132500&sparams=dur%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cnh%2Cpl%2Crequiressl%2Csource%2Cupn%2Cexpire&id=o-ANVqifMn-oLXQly4fQ-criwKxtoPVN725UIMxQ9DoudY&ip=115.118.104.11&mv=m&mt=1451667055&fexp=9408086%2C9408253%2C9416126%2C9416916%2C9418902%2C9419451%2C9420452%2C9421733%2C9422540%2C9422596%2C9423290%2C9423662%2C9423860%2C9424490%2C9425381%2C9426201%2C9426235&ms=au&dur=72.333&upn=CYqhI280wCA&key=yt6&mn=sn-cvh7zn7r&source=youtube&mm=31&signature=46E2ADD49ED635111E921A962B85BE8B7FBA6461.C6DA95E2F7110AA270E2C9B0B9EF07B6DF6636B5&lmt=1450123235816712&ipbits=0&itag=5&sver=3&mime=video%2Fx-flv&ratebypass=yes'

videolen = (60 + 13)*30
cap = cv2.VideoCapture(url)
cap.set(cv.CV_CAP_PROP_POS_FRAMES,0)
for i in range(0,videolen,100):
    cap.set(cv.CV_CAP_PROP_POS_FRAMES,i)
    frame = cap.read()
    cv2.imwrite( str(i) + '.jpg', frame[1] )
    print i
#pdb.set_trace()
