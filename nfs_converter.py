def convert_speed(speed, unit_in):


  conversion_factor = 1.60934  # Conversion factor between mph and kmph
  if unit_in == 'm':
    converted_speed = speed * conversion_factor
    unit_out = 'k'
  elif unit_in == 'k':
    converted_speed = speed / conversion_factor
    unit_out = 'm'
  else:
    converted_speed = None
    unit_out = None
    print("Error: Invalid unit. Please use 'm' for mph or 'k' for kmph.")

  return converted_speed, unit_out

def main():
  """Prompts the user for speed and unit, performs conversion, and displays results."""

  while True:
    unit_in = input("Enter the initial unit (m for mph or k for kmph): ").lower()
    if unit_in in ('m', 'k'):
      break
    else:
      print("Invalid unit. Please try again.")

  try:
    speed = float(input("Enter the speed value: "))
  except ValueError:
    print("Error: Please enter a valid number for speed.")
    return

  converted_speed, unit_out = convert_speed(speed, unit_in)

  if converted_speed is not None:
    print(f"{speed:.2f} {unit_in} is equal to {converted_speed:.2f} {unit_out}.")
  else:
    print("Conversion failed due to invalid unit input.")

if __name__ == "__main__":
  main()
