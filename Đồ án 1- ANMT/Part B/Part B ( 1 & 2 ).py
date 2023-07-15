from Functions import Encryptor, ShowFilesImported, hashlib, ShowFilesDecrypted, WriteToFiles_Kprivate, WriteToFiles_Kx_HKprivate,Decrypt, generateKey, Encrypt, ReadKey, get_random_bytes, os, ShowFiles, CheckExistingFiles

def main():
    while True:
        os.system("cls")
        choice = int(input("Bạn muốn:\n\t1. Mã hoá\n\t2. Giải mã\n\t3. Thoát\n===> Lựa chọn của bạn là: "))
        if choice == 1:
            os.system("cls")
            # Part 1
            # Người dùng chọn tập tin cần mã hoá (tập tin P)
            a = 0
            tenFile = ""
            while a == 0:
                ShowFiles()
                tenFile = str(input("\nMời bạn nhập tên file bạn muốn mã hoá bao gồm Extension (VD: abc.docx): "))
                if CheckExistingFiles(tenFile):
                    a = 1
                else:
                    print("File '" + tenFile + "' bạn nhập không có trong thư mục !!!\n")

            # Hệ thống phát sinh khoá bí mật Ks và mã hoá tập tin P thành tập tin C bằng thuật toán AES
            Ks = get_random_bytes(32)
            enc = Encryptor(Ks)
            enc.encrypt_file(str(tenFile))

            # Hệ thống phát sinh cặp khoá Kprivate và Kpublic của thuật toán RSA và mã hoá khoá Ks bằng khoá Kpublic, output là chuỗi Kx
            Kpublic, Kprivate = generateKey(512)
            msg = Ks.decode("latin-1")
            Kx = Encrypt(msg,int(Kpublic[1]),int(Kpublic[0]))

            # Hệ thống lưu lại chuỗi Kx kèm theo giá trị hash SHA-1 của Kprivate (gọi là HKprivate).
            # Có thể xuất thành file C.metadata, với C là tên của tập tin C ở trên, cấu trúc tập tin là tuỳ chọn (XML, JSON, Plain text…).
            m1 = hashlib.sha1()
            for s in Kprivate:
                m1.update(str(s).encode())
            HKprivate = m1.hexdigest()
            WriteToFiles_Kx_HKprivate(tenFile+".enc"+".metadata", Kx, HKprivate)
            
            # Hệ thống kết xuất khoá Kprivate cho người dùng (có thể xuất ra file).
            WriteToFiles_Kprivate("Kprivate.txt", Kprivate)
            print("\n=== Quá Trình Mã Hoá Thành Công ===")
            go = str(input("\nEnter để típ tục"))
        if choice == 2:
            os.system("cls")
            # Part 2
            # Người dùng chọn tập tin cần giải mã (tập tin C)
            a = 0
            tenFile2 = ""
            KprivateFromFile = []
            while a == 0:
                ShowFilesDecrypted()
                tenFile2 = str(input("\nMời bạn nhập tên file bạn muốn giải mã bao gồm Extension (VD: abc.docx): "))
                if CheckExistingFiles(tenFile2):
                    a = 1
                else:
                    print("\n===> File '" + tenFile2 + "' bạn nhập không có trong thư mục !!!\n")
            
            # Người dùng nhập khoá Kprivate (có thể chọn từ file)
            while True:
                os.system("cls")
                luachonKhoa = int(input(("Bạn muốn nhập khoá Kprivate từ: \n1. Bàn phím\n2. File\n===> Lựa chọn của bạn là: ")))
                if luachonKhoa == 1:
                    n = int(input("Mời bạn nhập n: "))
                    e = int(input("Mời bạn nhập e: "))
                    KprivateFromFile = [n,e]
                    break
                if luachonKhoa == 2:
                    ShowFilesImported()
                    tenFile = str(input("\nMời bạn nhập tên file Kprivate bạn muốn thêm bao gồm Extension (VD: abc.docx): "))
                    if CheckExistingFiles(tenFile):
                        if tenFile == "Kprivate.txt":
                            KprivateFromFile = ReadKey(tenFile, " ")
                            break
                        else:
                            print("\n===>File bạn nhập không có Key !!!")
                            go = str(input("\nEnter để típ tục"))
                    else:
                        print("\n===> File '" + tenFile + "' bạn nhập không có trong thư mục !!!\n")
                        go = str(input("\nEnter để típ tục"))
            
            # Hệ thống kiểm tra giá trị hash SHA-1 của Kprivate có trùng với HKprivate không?

            AESKeyEncrypted = ReadKey("t.txt.enc.metadata",' ')
            HKprivateRead = AESKeyEncrypted[len(AESKeyEncrypted)-1]
            AESKeyEncrypted = AESKeyEncrypted[:-1]

            m2 = hashlib.sha1()
            for s in KprivateFromFile:
                m2.update(str(s).encode())
            HKprivate2 = m2.hexdigest()
            
            if(HKprivateRead == HKprivate2):
            # Giải mã chuỗi Kx để có được Ks dùng Kprivate
                Ks2 = Decrypt(AESKeyEncrypted, int(KprivateFromFile[1]), int(KprivateFromFile[0])).encode("latin-1")

            # Dùng Ks giải mã tập tin C thành tập tin P
                dec = Encryptor(Ks2)
                dec.decrypt_file(tenFile2)
                print("\n=== Quá Trình Giải Mã Thành Công ===")
            else:
                print("\n=== Quá Trình Giải Mã Thất Bại ===")
            go = str(input("\nEnter để típ tục"))
        if choice == 3:
            break
        else:
            print("Lựa chọn không hợp lệ !!!")

main()


