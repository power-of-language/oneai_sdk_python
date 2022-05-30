import sys
import oneai.parsing as parsing

def comp4Test(a, b):
    return (a is None) == (b is None) and \
            a['separator'] == b['separator'] and \
            a['time'] == b['time'] and \
            a['preTime'] == b['preTime'] and \
            a['speaker'] == b['speaker'] and \
            a['weak'] == b['weak'] and \
            a['text'] == b['text']


parserTests = [
  {
    'input':"USER:",
    'output': 
    { 
      'weak': False,
      'preTime': False,
      'speaker': 'USER', 
      'time': False, 
      'separator': True, 
      'text':None
    }
  },
  {
    'input':"USER :",
    'output': 
    { 
      'weak': False,
      'preTime': False,
      'speaker': 'USER', 
      'time': False, 
      'separator': True, 
      'text':None
    }
  },
  {
    'input':"USER :asd",
    'output': 
    { 
      'weak': False,
      'preTime': False,
      'speaker': 'USER', 
      'time': False, 
      'separator': True, 
      'text':"asd"
    }
  },
  {
    'input':"USER 00:00 ",
    'output': 
    { 
      'weak': False,
      'preTime': False,
      'speaker': 'USER', 
      'time': True, 
      'separator': False, 
      'text':None
    }
  },
  {
    'input':"USER     :4:01/asdfilj 0:0",
    'output': 
    { 
      'weak': False,
      'preTime': False,
      'speaker': 'USER', 
      'time': False, 
      'separator': True, 
      'text':"4:01/asdfilj 0:0"
    }
  },
  {
    'input':"USER [00:00]",
    'output': 
    { 
      'weak': False,
      'preTime': False,
      'speaker': 'USER', 
      'time': True, 
      'separator': False, 
      'text':None
    }
  },
  {
    'input':"USER [00:00]:",
    'output': 
    { 
      'weak': False,
      'preTime': False,
      'speaker': 'USER', 
      'time': True, 
      'separator': True, 
      'text':None
    }
  },
  {
    'input':"[00:00] USER:",
    'output': 
    { 
      'weak': False,
      'preTime': True,
      'speaker': 'USER', 
      'time': False, 
      'separator': True, 
      'text':None
    }
  },
  {
    'input':"[00:00] USER:  asdfasdfa asd f asdf asd fasdf ",
    'output': 
    { 
      'weak': False,
      'preTime': True,
      'speaker': 'USER', 
      'time': False, 
      'separator': True, 
      'text':"asdfasdfa asd f asdf asd fasdf"
    }
  },
  {
    'input':" 00:00 USER  :  asdfasdfa asd f asdf asd fasdf ",
    'output': 
    { 
      'weak': False,
      'preTime': True,
      'speaker': 'USER', 
      'time': False, 
      'separator': True, 
      'text':"asdfasdfa asd f asdf asd fasdf"
    }
  },
  {
    'input':" 00:00 USER  :",
    'output': 
    { 
      'weak': False,
      'preTime': True,
      'speaker': 'USER', 
      'time': False, 
      'separator': True, 
      'text':None
    }
  },
  {
    'input':"AGENT 10:23  line 4.",
    'output': 
    { 
      'weak': False,
      'preTime': False,
      'speaker': 'AGENT', 
      'time': True, 
      'separator': False, 
      'text':"line 4."
    }
  },
  {
    'input':"AGENT -  line 4.",
    'output': 
    { 
      'weak': False,
      'preTime': False,
      'speaker': 'AGENT', 
      'time': False, 
      'separator': True, 
      'text':"line 4."
    }
  },
  {
    'input':"AGENT",
    'output': 
    { 
      'weak': True,
      'preTime': False,
      'speaker': 'AGENT', 
      'time': False, 
      'separator': False, 
      'text':None
    }
  }
]

inputTests=[
{
  'desc':"consistent 'SPEAKER  0:00' format",
  'text':"Prospect  0:00\nHello.\n\nAgent  0:01\nHi, Kiara. This is Almer with Acme. How are you doing?\n\nProspect  0:05\nYou're doing good from there. I didn't get it.\n\nAgent  0:09\nFrom Acme. We're a carrot platform I just was following up. It looks like you downloaded our whitepaper.\n\nProspect  0:15\nYeah. Look at it. Like.\n\nAgent  0:22\nYeah.\n\nProspect  0:23\nBut I really didn't get a chance to look at it yet.\n\nAgent  0:27\nYeah, no problem at all I just wanted to call to see, you know, if this is something that you're interested in, we could set up like, you know, 10 minutes for me to answer any questions that you have. Or if you want, we can see if it makes sense to, you know, set up like an actual flower of the product. But I wanted to reach out first and see what would be appropriate.\n\nProspect  0:49\nYeah, sure. I let me have a look into that. Actually, it sounded interesting to me, because we are also working on analytics here.\n\nAgent  0:59\nOf course, yeah. What are some of the things that you guys are looking for? I know, I mean, carrot soup, just as people become more data mature, you know, it becomes so important for, for companies to understand, you know, behavior of their users, and being able to track when there are event and things of that nature. So, yeah, I'd be happy to give you guys an overview. You want me to follow up like later this week? and then we can figure out, you know, timing is really like next week.\n\nProspect  1:28\nIf you Is it possible for you to call me on Friday by the time and have a look on the whole document which I have downloaded?\n\nAgent  1:36\nYeah. And we can have a more directed conversation for sure. What do you want me to give you a call at 1pm? I'm on pacific time as well.\n\nProspect  1:44\nYeah, 1pm would be fine. Okay,\n\nAgent  1:46\ncool. Sounds good. Well, I'll go ahead and add you on Farmvil. So you can put a name to the face and if anything changes, just let me know. But otherwise, I'll look forward to talking to you again on Friday.\n\nProspect  1:56\nYeah.\n\nAgent  1:58\nOkay, cool. Take care of on the way\n",
  'elements':16
  },
  {
  'desc':"consistent 'SPEAKER:' format",
  'text':"SPEAKER: I guess you can call me a musician, but a musician for me is somebody who has some training in this and a lot of what I do is self-taught.\nAGENT: I guess you can call me a musician, but a musician for me is somebody who has some training in this and a lot of what I do is self-taught.\nSPEAKER: I guess you can call me a musician, but a musician for me is somebody who has some training in this and a lot of what I do is self-taught.\nAGENT: I guess you can call me a musician, but a musician for me is somebody who has some training in this and a lot of what I do is self-taught.\nSPEAKER: I guess you can call me a musician, but a musician for me is somebody who has some training in this and a lot of what I do is self-taught.\n\n\n",
  'elements':5
  },{ 
  'desc':"missing pattern in utterance 3",
  'text':"SPEAKER: line 1.\nAGENT: number 2 line.\nSPEAKER: number 3 line.\nline 4.\nSPEAKER:line 5.\n\n\n",
  'elements':0
  },{ 
  'desc':"varying pattern, TIME+SEPARATOR appears in single utterance",
  'text':"SPEAKER: line 1.\nAGENT: number 2 line.\nSPEAKER: number 3 line.\nAGENT 10:23: line 4.\nSPEAKER:line 5.\n\n\n",
  'elements':5
  },{ 
  'desc':"varying pattern, time appears in single utterance",
  'text':"SPEAKER: line 1.\nAGENT: number 2 line.\nSPEAKER: number 3 line.\nAGENT 10:23 line 4.\nSPEAKER:line 5.\n\n\n",'elements':5
  },{ 
  'desc':"missing last content line in strong pattern",
  'text':"SPEAKER: line 1.\nAGENT: number 2 line.\nSPEAKER: number 3 line.\nAGENT 10:23 line 4.\nSPEAKER:",'elements':0
  },{ 
  'desc':"broken format afterwards speaker format",
  'text':"guess you can call me a musician, but a musician for me is somebody who has some training in this and a lot of what I do is self-taught.\nAGENT: I guess you can call me a musician, but a musician for me is somebody who has some training in this and a lot of what I do is self-taught.\nSPEAKER: I guess you can call me a musician, but a musician for me is somebody who has some training in this and a lot of what I do is self-taught.\nAGENT: I guess you can call me a musician, but a musician for me is somebody who has some training in this and a lot of what I do is self-taught.\nSPEAKER: I guess you can call me a musician, but a musician for me is somebody who has some training in this and a lot of what I do is self-taught.\n\n\n",'elements':0
  },{ 
  'desc':"Weak speaker, no separtor",
  'text':"SPEAKER\n line 1.\nAGENT\n number 2 line.\nSPEAKER\n number 3 line.\nAGENT 10:23: line 4.\nSPEAKER\nline 5.\n\n\n",'elements':5
  },{ 
  'desc':"Weak speaker, no separtor, missing last line",
  'text':"SPEAKER\n line 1.\nAGENT\n number 2 line.\nSPEAKER\n number 3 line.\nAGENT 10:23: line 4.\nSPEAKER\n",'elements':0
  },{ 
  'desc':"Weak speaker but too short",
  'text':"SPEAKER\n line 1.\nAGENT\n number 2 line.",'elements':0
  },{ 
  'desc':"2nd utterance is weak speaker but too short",
  'text':"SPEAKER:\n line 1.\nAGENT\n number 2 line.",'elements':0
  },{ 
  'desc':"short strong pattern",
  'text':"SPEAKER:\n line 1.\nAGENT:\n number 2 line.",'elements':2
  },{ 
  'desc':"weak pattern - studio chatbot example",
  'text':"USER\nI would like a shared cab to get to Gallo's, hurry please.\n\nSYSTEM\nHow many people are in your group?\n\nUSER\nThere are two people.\n\nSYSTEM\nSorry, I didn't get that. could you please repeat?\n\nUSER\nCome on! we are two people. two.stupid bot.\n\nSYSTEM\nYou want a shared ride for 2 people to Gallo's. Is that right?\n\nUSER\nYes, yes, that is right. Can you tell me how long the ride takes and it's cost?\n\nSYSTEM\nYour cab is confirmed and is coming for you right now. The ride duration is 32 minutes and costs $22.81.\n\nUSER\nOh yes, this is excellent. Thank you!\n",
  'elements':9
  },{ 
  'desc':"weak pattern long with underscores",
  'text':"USER_USER_USER\nI would like a shared cab to get to Gallo's, hurry please.\n\nSYSTEM\nHow many people are in your group?\n\nUSER\nThere are two people.\n\nSYSTEM\nSorry, I didn't get that. could you please repeat?\n\nUSER\nCome on! we are two people. two.stupid bot.\n\nSYSTEM\nYou want a shared ride for 2 people to Gallo's. Is that right?\n\nUSER\nYes, yes, that is right. Can you tell me how long the ride takes and it's cost?\n\nSYSTEM\nYour cab is confirmed and is coming for you right now. The ride duration is 32 minutes and costs $22.81.\n\nUSER\nOh yes, this is excellent. Thank you!\n",
  'elements':9
  }
]

def runTests():
    print('running tests...')
    for i, test in enumerate(parserTests):
        print(f'test 1.{i} -', test['input'])
        parsedSpeaker = parsing._parseSpeakerLine(test['input'])
        if not parsedSpeaker or not comp4Test(parsedSpeaker, test['output']):
            print(f'failed input 1.{i}: ', test['input'])
            print('expected output:', test['output'])
            print('actual output:', parsedSpeaker)
            
            raise Exception()

    for i, test in enumerate(inputTests):
        print(f'test 2.{i} -', test['desc'])
        try: parsed = parsing.parse_conversation(test['text'])
        except Exception as e:
            if test['elements'] > 0:
                print(f'failed input 2.{i}: ', test['text'])
                print('expected output:', test['elements'])
                print('actual output:', e)
            continue
        if not parsed or not parsed.utterances:
            print(f'failed input: 2.{i}', test['input'])
            print('expected elements:', test['elements'])
            print('actual output:', parsed)
        if len(parsed.utterances) != test['elements']:
            print(f'failed input: 2.{i}', test['input'])
            print('expected elements:', test['elements'])
            print('actual elements:', len(parsed))

    print('tests OK')

runTests()
