order_slots = ['rest', 'meal', 'confirm', 'end']

def response_order(slot, entities=None):
    if slot == 'rest':
        return '请选择一个餐厅'
    elif slot == 'meal':
        return '请选择您喜欢的一个餐品'
    elif slot == 'confirm':
        return '确定提交吗？'
    else:
        return '已为您提交所选餐品'

