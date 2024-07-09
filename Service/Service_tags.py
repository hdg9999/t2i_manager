
### Tag 예시 ###
# -> {'태그명':{'$eq':True}}
# 요런 형태로 안들어오면 뭔가 잘못 된 것임.
def selected_tags_formatter(tag:dict):
    return next(iter(tag))
