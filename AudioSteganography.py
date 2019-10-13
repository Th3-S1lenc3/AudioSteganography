import wave
import sys
import time

def menu():
    print("Audio Steganography Tool V1.0")
    print("1. Encode a message")
    print("2. Decode a message")
    print("3. Read Me \n")

    choice = input("Enter your choice here (1,2,3): ")

    if choice == "1":
        encode()
    if choice == "2":
        decode()
    if choice == "3":
        ReadMe()
    else:
        print("Invalid Input. Please enter 1, 2, or 3.")
        menu()

def encode():
    print("PLEASE ENSURE THAT THE SOURCE AUDIO FILE IS IN THE SAME FILE LOCATION AS THIS SCRIPT! \n")
    # Asks user for the file name
    input_file = input("Enter the name of the source file (with the .wav file extension): ")
    # read wave audio file
    song = wave.open(input_file, mode='rb')
    # Read frames and convert to byte array
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))

    # The "secret" text message
    string = input("Please enter the secret message you wish to encode: ")
    # Append dummy data to fill out rest of the bytes. Receiver shall detect and remove these characters.
    string = string + int((len(frame_bytes)-(len(string)*8*8))/8) *'#'
    # Convert text to bit array
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in string])))

    # Replace LSB of each byte of the audio data by one bit from the text bit array
    for i, bit in enumerate(bits):
        frame_bytes[i] = (frame_bytes[i] & 254) | bit
    # Get the modified bytes
    frame_modified = bytes(frame_bytes)

    # Write bytes to a new wave audio file
    output_file = input("Please specify the name of the output file  (with the .wav extension): ")
    with wave.open(output_file, 'wb') as fd:
        fd.setparams(song.getparams())
        fd.writeframes(frame_modified)
    song.close()

    print(output_file + " Successfully Generated. \n")

    Continue()


def decode():
    print("PLEASE ENSURE THAT THE FILE YOU WISH TO DECODE IS IN THE SAME FILE LOCATION AS THIS SCRIPT! \n")
    # Asks user for the file name
    input_file = input("Enter the name of the file (with the .wav file extension): ")
    song = wave.open(input_file, mode='rb')
    # Convert audio to byte array
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))

    # Extract the LSB of each byte
    extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
    # Convert byte array back to string
    string = "".join(chr(int("".join(map(str, extracted[i:i + 8])), 2)) for i in range(0, len(extracted), 8))
    # Cut off at the filler characters
    decoded = string.split("###")[0]

    # Print the extracted text
    print("Sucessfully decoded: " + decoded)
    song.close()

    Continue()

def ReadMe():
    print("Audio Steganography Tool V1.0")
    print("Coded by TH3_S1LENC3 and using code from "
          "https://medium.com/@sumit.arora/audio-steganography-the-art-of-hiding-secrets-within-earshot-part-2-of-2"
          "-c76b1be719b3.")
    print("This tool is designed to embedded or extract messages hidden in audio files.")
    print("It is imperative that all files inputted end with .wav.")
    print("Please enjoy using this tool. And Have Fun Hiding Messages in Audio.")
    time.sleep(5)
    menu()

def Continue():
    choice = input("Do you wish to encode/decode another file (Yes/No): ")
    choice = choice.lower()

    if choice == "yes":
        menu()
    if choice == "no":
        sys.exit(0)
    else:
        print("Please enter Yes or No. \n")
        Continue()

menu()
