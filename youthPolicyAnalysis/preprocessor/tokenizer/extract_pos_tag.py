from konlpy.tag import Mecab

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