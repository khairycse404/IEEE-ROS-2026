def safe_divide():
    try:
        num1 = float(input("Enter the 1st number: "))
        num2 = float(input("Enter the 2nd number: "))
        
        result = num1 / num2
        print("Result:", result)
    
    except ValueError:
        print("Enter numbers only")
    
    except ZeroDivisionError:
        print("You cannot divide by zero.")

safe_divide()