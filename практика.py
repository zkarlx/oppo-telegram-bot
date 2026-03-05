SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.'

rezhim = input("Режимді таңдаңыз (encrypt/decrypt): ")
message = input("Хабарлама: ")
key = int(input("Кілт: "))

translated = ""

for symbol in message:
    if symbol in SYMBOLS:
        symbolIndex = SYMBOLS.find(symbol) #символ индексін табу

        if rezhim == "encrypt":
            newIndex = (symbolIndex + key) % len(SYMBOLS)
        elif rezhim == "decrypt":
            newIndex = (symbolIndex - key) % len(SYMBOLS)
        else:
            print("Қате режим!")
            break

        translated += SYMBOLS[newIndex] #жаңа индекстегі символды алып нәтижеге қосамыз
    else:
        translated += symbol

print("Нәтиже:")
print(translated)


