import difflib
from dateutil import parser
from dateutil.tz import gettz
import sys

date_format = "%d/%m/%Y" #adjustable

months = {
    'januari': 'january', 
    'februari': 'february', 
    'maret': 'march', 
    'april': 'april', 
    'mei': 'may', 
    'juni': 'june', 
    'juli': 'july', 
    'agustus': 'august', 
    'september': 'september', 
    'oktober': 'october', 
    'november': 'november', 
    'desember': 'december'
  }


nums = {
    'satu': {
        'num': 1,
        'op': None,
        'type': 'base'
    },
    'dua': {
        'num': 2,
        'op': None,
        'type': 'base'
    },
    'tiga': {
        'num': 3,
        'op': None,
        'type': 'base'
    },
    'empat': {
        'num': 4,
        'op': None,
        'type': 'base'
    },
    'lima': {
        'num': 5,
        'op': None,
        'type': 'base'
    },
    'enam': {
        'num': 6,
        'op': None,
        'type': 'base'
    },
    'tujuh': {
        'num': 7,
        'op': None,
        'type': 'base'
    },
    'delapan': {
        'num': 8,
        'op': None,
        'type': 'base'
    }, 
    'sembilan': {
        'num': 9,
        'op': None,
        'type': 'base'
    },
    'sepuluh': {
        'num': 10,
        'op': None,
        'type': 'base'
    },
    'sebelas': {
        'num': 11,
        'op': None,
        'type': 'base'
    },
    'seratus': {
        'num': 100,
        'op': None,
        'type': 'base'
    },
    'seribu': {
        'num': 1000,
        'op': None,
        'type': 'base'
    },

    'belas': {
        'num': 10,
        'op': 'add',
        'type': 'sym'
    },
    'puluh': {
        'num': 10,
        'op': 'multiple',
        'type': 'sym'
    },
    'ratus': {
        'num': 100,
        'op': 'multiple',
        'type': 'sym'
    },
    'ribu': {
        'num': 1000,
        'op': 'multiple',
        'type': 'sym'
    }
}




# find the highest score 
def month_corrector(mo_token):
  higest = 0
  fix_mo = ''
  for key, val in months.items():
    seq = difflib.SequenceMatcher(None, mo_token, key)
    seq = seq.quick_ratio()*100
    if seq > higest:
      higest = seq
      fix_mo = val

  return fix_mo, higest



def str_to_num(strnum):
  res, temp, temp2 = 0, 0, 0
  error_message = ''

  strdate = strnum.split()
  dlist = [i for i in range(len(strdate))]
  for idx, d in enumerate(strdate):
    if d not in nums:
      error_message = 'Whoops! looks like any typo. Please recheck.'
      print(error_message)
      sys.exit()
    else:
      for key, val in nums.items():
        if d == key and val.get('type') == 'sym':
          temp = nums.get(d).get('num') * nums.get(strdate[idx-1]).get('num') if val.get('op') == 'multiple' else nums.get(d).get('num') + nums.get(strdate[idx-1]).get('num')
          res = res + temp
          dlist = [x for x in dlist if (x not in [idx, idx-1])]
  for rest in dlist:
    temp2 = nums.get(strdate[rest]).get('num')
    res = res + temp2

  return res




def date_to_num(date_token):
  datestring = ' '.join([i for i in date_token])

  hscore = 0
  for month in date_token:
    mo, score = month_corrector(month) 
    if score > hscore:
      hmonth = month.lower()
      hscore = score

  day = datestring.lower().split(hmonth)[0]
  year = datestring.lower().split(hmonth)[1]

  day_num = str_to_num(day)
  year_num = str_to_num(year)

  return str(day_num), hmonth, str(year_num)




# the core code
def date_standardizer(date_token):
  date_token = date_token.split()
  
  if len(date_token) > 2:
    if any(i.isdigit() for i in date_token):
      day_token = date_token[0].lower()
      mo_token = date_token[1] if date_token[1].lower().isnumeric() else month_corrector(date_token[1].lower())[0]
      year_token = date_token[2].lower()
      
      date_eng_format = day_token + ' ' + mo_token + ' ' + year_token
    
    else:
      day, month, year = date_to_num(date_token)
      date_eng_format = str(day) + " " + month_corrector(month)[0] + " " + str(year)
  else:
    date_eng_format = date_token[0]

  try:
    tzinfos = {"ICT": gettz("Asia/Jakarta")}
    final_date = parser.parse(date_eng_format, 
                              tzinfos=tzinfos, 
                              dayfirst=True).strftime("%d/%m/%Y")
  except ValueError:
    final_date = "Format yang dimasukkan salah."

  return final_date


print("Pola tanggal berbahasa indonesia hari-bulan-tahun, format bebas, contoh: ")
print("-28 juni 1987")
print("-dua november seribu sembilan ratus sembilan puluh lima")


date_input = input("\nMasukkan input tanggal: ")

print("-"*20)
print("Hasil standarisasi: ", date_standardizer(date_input))