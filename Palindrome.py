##############STEPHEN LUKE TODD
#############ADVANCED DATA STRUCTURES 
from Deque import*

def Palindrome(string):
    char_deque = Deque()

    for ch in string:
        char_deque.add_rear(ch)

    still_equal = True

    while char_deque.size() < 1 and still_equal == True:
        first = char_deque.remove_front()
        last = char_deque.remove_rear()
        
        if first != last:
            still_equal = False

    return still_equal

print(Palindrome("sus"))
print(Palindrome("moom"))
print(Palindrome("pokekop"))


    
