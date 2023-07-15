from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os.path
import hashlib
import random, os
from os.path import exists

# AES
class Encryptor:
    def __init__(self, key):
        self.key = key

    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message, key, key_size=256):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext, self.key)
        with open(file_name + ".enc", 'wb') as fo:
            fo.write(enc)
        os.remove(file_name)

    def decrypt(self, ciphertext, key):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")

    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, self.key)
        with open(file_name[:-4], 'wb') as fo:
            fo.write(dec)
        os.remove(file_name)
# AES - end

# RSA
def power(a, n, p):
    res = 1
    a = a % p 

    while n > 0:         
        if n % 2:
            res = (res * a) % p
            n = n - 1
        else:
            a = (a ** 2) % p
            n = n // 2
             
    return res % p

def gcd(a, b):
   while a != 0:
      a, b = b % a, a
   return b

def findModInverse(a, m):
   if gcd(a, m) != 1:
      return None
   u1, u2, u3 = 1, 0, a
   v1, v2, v3 = 0, 1, m
   
   while v3 != 0:
    q = u3 // v3
    v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
   return u1 % m
     
def isPrime(n, k):
    if n == 1 or n == 4:
        return False
    elif n == 2 or n == 3:
        return True
    else:
        for i in range(k):             
            # Chọn 1 số ngẫu nhiên trong [2..n-2] Để đảm bảo rằng n luôn lớn hơn 4
            a = random.randint(2, n - 2)
             
            # Fermat nhỏ
            if power(a, n - 1, n) != 1:
                return False                 
    return True

def generateLargePrime(keysize):
   while True:
      num = random.randrange(2**(keysize-1), 2**(keysize))
      if isPrime(num, 3):
         return num

def generateKey(keySize):
   p = generateLargePrime(keySize)
   q = generateLargePrime(keySize)
   n = p * q
	
   while True:
      e = random.randrange(2 ** (keySize - 1), 2 ** (keySize))
      if gcd(e, (p - 1) * (q - 1)) == 1:
         break

   d = findModInverse(e, (p - 1) * (q - 1))
   publicKey = (n, e)
   privateKey = (n, d)
   print("- Quá trình tạo khoá \n====> Thành công !!!")
   return (publicKey, privateKey)

def Encrypt(msg,e,n):
    luuchuoi = []
    for i in msg:
        c = power(ord(i),e,n)
        luuchuoi.append(str(c))
    return luuchuoi

def Decrypt(luuchuoi, d, n):
    msg2 = ""
    for i in luuchuoi:
        de = power(int(i),d,n)
        msg2+=chr(de)
    return msg2
# RSA - end

# Check Existing Files:
def CheckExistingFiles(fileName):
    if (os.path.exists(fileName)):
        return True
    
# Show All Files Which Can Be Encrypted In Directories: 
def ShowFiles():
    files = os.listdir("C:\\Users\\ADMIN\\OneDrive\\Máy tính\\BT3\\Alice")
    input_argument = (".docx", ".txt")

    files = sorted(files) 

    relevant_files = []
    for file_name in files:
        if file_name.endswith(input_argument):
            relevant_files.append(file_name)
    print ("Các Files có thể mã hoá đang tồn tại trong thư mục: " + str(relevant_files))

# Show All Files Which Can Be Decrypted In Directories: 
def ShowFilesDecrypted():
    files = os.listdir("C:\\Users\\ADMIN\\OneDrive\\Máy tính\\BT3\\Alice")
    input_argument = ".enc"

    # Sort file names by name
    files = sorted(files) 

    relevant_files = []
    for file_name in files:
        # Your Conditions goes here ........
        if file_name.endswith(input_argument):
            relevant_files.append(file_name)
    print ("Các Files có thể giải mã đang tồn tại trong thư mục: " + str(relevant_files))

# Show Menu
def Menu():
    print("=== LỰA CHỌN ===")
    print("\n1. Cho phép phát sinh một khoá bí mật Ks của thuật toán AES\n2. Mã hoá tập tin sử dụng thuật toán AES với khoá Ks")
    print("3. Giải mã tập tin sử dụng thuật toán AES với khoá Ks\n4. Phát sinh một cặp khoá Kprivate và Kpublic của thuật toán RSA")
    print("5. Mã hoá một chuỗi sử dụng thuật toán RSA sử dụng khoá Kpublic\n6. Giải mã một chuỗi sử dụng thuật toán RSA sử dụng khoá Kprivate")
    print("7. Tính giá trị hash của một chuỗi sử dụng thuật toán SHA-1, SHA-256 \n8.Thoát\n")

# main
def main():
    keyAES = 0
    publicKey = 0
    privateKey = 0
    chuoiEncrypted = []
    while True:
        os.system('cls')
        Menu()
        luachon = int(input("==> Mời bạn nhập lựa chọn: "))
        if luachon > 0 and luachon <= 8:
            if luachon == 1:
                os.system('cls')
                print ("=== Phát sinh một khoá bí mật Ks của thuật toán AES === \n")
                keyAES = get_random_bytes(32)
                enc = Encryptor(keyAES)
                print(keyAES)
                print("\n ===> Quá trình tạo khoá Ks trong thuật AES thành công  ")
                go = str(input("\nNhấn Enter để tiếp tục !!!"))
            if luachon == 2:
                if keyAES == 0:
                    print("Key dùng để mã hoá tập tin bằng thuật toán AES không có !!!\nMời bạn nhập lại lựa chọn 1 để tạo khoá AES trước !!!")
                    continue
                else:
                    a = 0
                    os.system('cls')
                    print ("=== Mã hoá tập tin sử dụng thuật toán AES với khoá Ks === \n")
                    while a == 0:
                        ShowFiles()
                        tenFile = str(input("\nMời bạn nhập tên file bạn muốn mã hoá bao gồm Extension (VD: abc.docx): "))
                        if CheckExistingFiles(tenFile):
                            a = 1
                        else:
                            print("File '" + tenFile + "' bạn nhập không có trong thư mục !!!\n")
                    enc.encrypt_file(str(tenFile))
                    print("\n===> Quá trình mã hoá tập tin '" + tenFile + "' thành công")
                    go = str(input("\nNhấn Enter để tiếp tục !!!"))
            if luachon == 3:
                if keyAES == 0:
                    print("Key dùng để giải mã tập tin bằng thuật toán AES không có !!!\nMời bạn nhập lại tuần tự lựa chọn 1 và 2 để tạo khoá AES và mã hoá tập tin trước !!!")
                    continue
                else:
                    a = 0
                    os.system('cls')
                    print("===  Giải mã tập tin sử dụng thuật toán AES với khoá Ks ===\n")
                    while a == 0:
                        ShowFilesDecrypted()
                        tenFile = str(input("\nMời bạn nhập tên file bạn muốn giải mã bao gồm Extension (VD: abc.docx.enc): "))
                        if CheckExistingFiles(tenFile):
                            a = 1
                        else:
                            print("File '" + tenFile + "' bạn nhập không có trong thư mục !!!\n")
                    enc.decrypt_file(str(tenFile))
                    print("\n===> Quá trình giải mã tập tin '" + tenFile + "' thành công")
                    go = str(input("\nNhấn Enter để tiếp tục !!!"))
            if luachon == 4:
                if publicKey == 0:
                    os.system('cls')
                    print("===  Phát sinh một cặp khoá Kprivate và Kpublic của thuật toán RSA ===\n")
                    publicKey, privateKey = generateKey(512)
                    print("\nPublicKey: "+ str(publicKey))
                    print("\nPrivateKey: "+ str(privateKey))
                    go = str(input("\nNhấn Enter để tiếp tục !!!"))
                else:
                    print("Đã tồn tại cặp khoá PublicKey và PrivateKey !!!")
                    go = str(input("\nNhấn Enter để tiếp tục !!!"))
            if luachon == 5:
                if publicKey == 0:
                    print("Key dùng để mã hoá chuỗi bằng thuật toán RSA không có !!!\nMời bạn nhập lại lựa chọn 4 để tạo cặp khoá RSA trước !!!")
                    go = str(input("\nNhấn Enter để tiếp tục !!!"))
                    continue
                else:
                    os.system('cls')
                    print("===  Mã hoá một chuỗi sử dụng thuật toán RSA sử dụng khoá Kpublic ===\n")
                    chuoi = str(input("Mời bạn nhập chuỗi muốn mã hoá: "))
                    chuoiEncrypted = Encrypt(chuoi, publicKey[1],publicKey[0])
                    print("\nChuỗi sau khi đã mã hoá: " + str(chuoiEncrypted))
                    print ("\n===> Mã hoá thành công")
                    go = str(input("\nNhấn Enter để tiếp tục !!!"))
            if luachon == 6:
                if publicKey == 0:
                    print("Key dùng để mã hoá chuỗi bằng thuật toán RSA không có !!!\nMời bạn nhập lại lựa chọn 4 để tạo cặp khoá RSA trước !!!")
                    go = str(input("\nNhấn Enter để tiếp tục !!!"))
                    continue
                elif chuoiEncrypted == []:
                    print("Không tồn tại chuỗi đã mã hoá !!!\n Mời bạn nhập lại lựa chọn 5 để tạo chuỗi mã hoá bằng RSA trước !!!")
                    go = str(input("\nNhấn Enter để tiếp tục !!!"))
                    continue
                else:
                    os.system('cls')
                    print("===  Giải mã một chuỗi sử dụng thuật toán RSA sử dụng khoá Kprivate ===\n")
                    chuoiDecrypted = Decrypt(chuoiEncrypted, privateKey[1],privateKey[0])
                    print("Chuỗi sau khi đã giải mã: " + str(chuoiDecrypted))
                    print ("\n===> Giải mã thành công")
                    go = str(input("\nNhấn Enter để tiếp tục !!!"))
            if luachon == 7:
                os.system('cls')
                print("===  Tính giá trị hash của một chuỗi sử dụng thuật toán SHA-1, SHA-256 ===\n")
                chuoi = str(input("Mời bạn nhập chuỗi muốn hash: "))
                m1 = hashlib.sha1(chuoi.encode('UTF-8'))
                print("\nGiá trị Hash của chuỗi sau khi được hash bằng SHA-1: "+ m1.hexdigest())  
                m256 = hashlib.sha256(chuoi.encode('UTF-8'))
                print("\nGiá trị Hash của chuỗi sau khi được hash bằng SHA-256: "+ m256.hexdigest())  
                print ("\n===> Hash thành công")
                go = str(input("\nNhấn Enter để tiếp tục !!!"))
            if luachon == 8:
                break
        else:
            print("Lựa chọn của bạn không hợp lệ !!!")
            go = str(input("\nNhấn Enter để tiếp tục !!!"))

main()