from konlpy.tag import Mecab

#mecab을 찾지 못하는 에러로 인한 절대 경로로 지정함 
def noun_tagging(df) :
  #mecab = Mecab()
  mecab = Mecab('C:\mecab\share\mecab-ko-dic')
  return df.apply(lambda x: [mecab.nouns(word) for word in x])