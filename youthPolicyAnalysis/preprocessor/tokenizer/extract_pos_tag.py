from konlpy.tag import Mecab, Okt

#mecab을 찾지 못하는 에러로 인한 절대 경로로 지정함 
def noun_tagging(df) :
  #mecab = Mecab()
  mecab = Mecab('C:\mecab\share\mecab-ko-dic')
  return df.apply(lambda x: [mecab.nouns(word) for word in x])

def verb_tagging(df) :
  mecab = Mecab('C:/mecab/share/mecab-ko-dic')
  parsed = mecab.pos(df)
  verbs = [word for word, pos in parsed if pos.startswith('VV')]  # VV는 동사
  return verbs

def adjective_tagging(df) :
  mecab = Mecab('C:/mecab/share/mecab-ko-dic')
  parsed = mecab.pos(df)
  adjectives = [word for word, pos in parsed if pos == 'VA']  # VV는 동사
  return adjectives


# Okt 객체 생성
okt = Okt()

# 동사 추출 함수
def okt_verb_tagging(sentence):
    parsed = okt.pos(sentence)
    verbs = [word for word, pos in parsed if pos == 'Verb']  # Verb는 동사
    return verbs

# 형용사 추출 함수
def okt_adjective_tagging(sentence):
    parsed = okt.pos(sentence)
    adjectives = [word for word, pos in parsed if pos == 'Adjective']  # Adjective는 형용사
    return adjectives