import math

def solve_quadratic(a, b, c):
    # Calculate discriminant
    D = b**2 - 4*a*c

    if D > 0:
        x1 = (b + math.sqrt(D)) / (2*a)
        x2 = (b - math.sqrt(D)) / (2*a)
        print("Two real roots:")
        print(f"x₁ = {x1}")
        print(f"x₂ = {x2}")
        return x1, x2
    elif D == 0:
        x = b / (2*a)
        print("One real root:")
        print(f"x = {x}")
        return x, x
    else:
        real_part = b / (2*a)
        imag_part = math.sqrt(-D) / (2*a)
        x1 = complex(real_part, imag_part)
        x2 = complex(real_part, -imag_part)
        print("Complex roots:")
        print(f"x₁ = {x1}")
        print(f"x₂ = {x2}")
        return x1, x2

# --- Fixed coefficients ---
a = 8700.0
b = 435.0

print("Quadratic Equation: 8700x^2 - 435x + c = 0")
c = float(input("Enter value of c: "))

# --- Solve ---
x1, x2 = solve_quadratic(a, b, c)

# --- Example operation using x2 ---
A = 1 * x2
print(f"\nA = 1 * x₂ = {A}")
Astx = A*1000*359
space = (1000*16*math.pi)/Astx
print(Astx)
print(space)