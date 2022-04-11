from tasks import longtime_add
import time


if __name__ == '__main__':
    url = ['http://www.yahoo.com' , 'http://google.com'] # change them to your ur list.
    for i in url:
        result = longtime_add.delay(i)
        print ('Task result:', result)