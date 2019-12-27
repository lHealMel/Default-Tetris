i = 0
while i <= 100:
    i = + 1
    list = open("C:/Users/ADMIN/Desktop/리스트.txt", 'a')
    name = input("학번을 적어주세요: ")
    list.write(name)
    list.write(":")
    number = input("점수를 적어주세요: ")
    list.write(number)
    list.write("\n")
    list.close()
