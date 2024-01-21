import pyfiglet
from termcolor import colored

def text_to_colored_banner(input_text, color="red", font="standard"):
    banner = pyfiglet.figlet_format(input_text, font=font)
    colored_banner = colored(banner, color)
    print(colored_banner)

# Example usage
text_to_colored_banner("Network Scanner", color="red", font="standard")

