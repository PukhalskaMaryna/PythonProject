from string import punctuation

def is_palindrome(text):
    text = text.lower().replace(' ','')
    for symbol in punctuation:
        text = text.replace(symbol,'')
    return text[::-1] == text

assert is_palindrome('A man, a plan, a canal: Panama') == True, 'Test1' 
assert is_palindrome('0P') == False, 'Test2' 
assert is_palindrome('a.') == True, 'Test3' 
assert is_palindrome('aurora') == False, 'Test4' 
print("ОК")