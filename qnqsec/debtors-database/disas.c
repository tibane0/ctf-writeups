void menu() {
	void* fsbase;
	int64_t var_10 = *(fsbase + 0x28);

	while (true);
	    putchar(0xa);
	    puts("Debtors' Database v2.1");
	    puts("What do you want to do today?\n");
	    puts("1. Show namelist");
	    puts("2. Input name");
	    puts("3. Delete name");
	    puts("4. Admin menu");
	    printf(&data_402263);
	    void input;
	    fgets(&input, 4, stdin);
	    fflush(stdin);
	    putchar(0xa);
	    int32_t choice = atoi(&input);
	
	    if (choice == 4)
	        break;
	
	    if (choice == 3)
	        remove_name();
	        continue;
	    else if (choice == 1)
	        show_namelist();
	        continue;
	    else if (choice == 2)
	        input_name();
	        continue;

	    puts("Invalid input!");
	    puts("Press ENTER to go back...");
	    getchar();
	enter_password();
	exit(status: 0);
	noreturn;
}

int main() {
	void* fsbase
	int64_t canary = *(fsbase + 0x28)
	setup()
	puts("What is your name (9 chars or le…")
	void name
	fgets(&name, 0xa, stdin)
	printf("Hello, ")
	printf(&name)  // format string
	putchar(0xa)
	fflush(stdin)
	menu()
	noreturn
}

void show_namelist() {
	puts("[Index]        | [Amt]       | […")

	for (int32_t i = 0; i s<= 0x13; i += 1)
	    if (*((sx.q(i) << 3) + &namelist) == 0)
	        printf("Index #%d  | EMPTY\n", zx.q(i))
	    else
	        printf("Index #%d  | $%d  | %s\n", zx.q(i), 
	            zx.q(*(*((sx.q(i) << 3) + &namelist) + 0x80)), 
	            *((sx.q(i) << 3) + &namelist))

	puts("Press ENTER to return.")
	return getchar()
}



int64 input_name() {
	void* fsbase
	int64_t rax = *(fsbase + 0x28)
	puts("Adding a new entry.")
	puts("Which index do you want to input…")
	char buf[0x80]
	fgets(&buf, 4, stdin)
	int32_t index = atoi(&buf)
	fflush(stdin)

	if (index s> 0x13 || index s< 0)
	    puts("Invalid index!")
	    puts("Press ENTER to go back...")
	    getchar()
	else
	    puts("Enter debtor's name:")
	    fgets(&buf, 0x80, stdin)
	    buf[strcspn(&buf, &data_4020ef, &data_4020ef)] = 0
	    void debtors_name
	    // check for buffer overflow
	    strcpy(&debtors_name, &buf, &buf)
	    fflush(stdin)
	    puts("Enter the amount owed:")
	    fgets(&buf, 0xa, stdin)
	    int32_t amount_owed = atoi(&buf)
	    fflush(stdin)
	    *((sx.q(index) << 3) + &namelist) = malloc(0x84)
	    *(*((sx.q(index) << 3) + &namelist) + 0x80) = amount_owed
	    int64_t name = *((sx.q(index) << 3) + &namelist)
	    strcpy(name, &debtors_name, name)
	    puts("Name inputted.")
	    printf("%s owes %d, added to slot #%d.\n", *((sx.q(index) << 3) + &namelist), 
	        zx.q(*(*((sx.q(index) << 3) + &namelist) + 0x80)), zx.q(index))
	    puts("Press ENTER to return.")
	    getchar()

	if (rax == *(fsbase + 0x28))
	    return rax - *(fsbase + 0x28)

	__stack_chk_fail()
	noreturn
}

int64_t remove_name() {
	void* fsbase;
	int64_t rax = *(uint64_t*)((char*)fsbase + 0x28);
	puts("Which name would you like to rem…");
	void buf;
	fgets(&buf, 4, stdin);
	fflush(stdin);
	int32_t index = atoi(&buf);

	if (index < 0 || index > 0x13)
	{
	    puts("Invalid index!");
	    puts("Press ENTER to go back...");
	    getchar();
	}
	else if (!*(uint64_t*)(((int64_t)index << 3) + &namelist))
	    puts("The index is empty!");
	else
	{
	    void name;
	    strcpy(&name, *(uint64_t*)(((int64_t)index << 3) + &namelist));
	    free(*(uint64_t*)(((int64_t)index << 3) + &namelist));
	    printf("Name %s at index #%d has been re…", &name, (uint64_t)index);
	}

	if (rax == *(uint64_t*)((char*)fsbase + 0x28))
	    return rax - *(uint64_t*)((char*)fsbase + 0x28);

	__stack_chk_fail();
	/* no return */
}


void enter_password() {
void* fsbase;
int64_t canary = *(uint64_t*)((char*)fsbase + 0x28);
printf("\nPlease enter the password for …");
void password;  // buffer overflow
fgets(&password, 0x100, stdin);
puts("\nWrong password!");
*(uint64_t*)((char*)fsbase + 0x28);

if (canary == *(uint64_t*)((char*)fsbase + 0x28))
    return 0;

__stack_chk_fail();
}



