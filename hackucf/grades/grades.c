#include <stdio.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>


/*
 * This is the correct and proper way to implement MIN() in C.
 * There are no bugs here and this is not part of the challenge.
 */
#define MIN(a, b) ({ \
	__typeof__(a) _a = (a); \
	__typeof__(b) _b = (b); \
	_a < _b ? _a : _b; \
})


struct userdata {
	char grade[4];
	int age;
	char firstName[100];
	char lastName[100];
};

char* read_line(char* buf, size_t bufsize) {
	if(!fgets(buf, bufsize, stdin)) {
		exit(EXIT_FAILURE);
	}
	
	char* end = strchr(buf, '\n');
	if(end) {
		*end = '\0';
	}
	
	return buf;
}

/* DON'T FORGET TO REMOVE THIS FUNCTION AFTER TESTING! */
void todo_remove_this_function(const char* cmd) {
	system(cmd);
}


int main(void) {
	/*
	 * I'm getting good at C programming now!!! My code is so secure!
	 * Just look at all the sizeof()s!
	 */
	
	struct userdata user;
	memset(&user, 0, sizeof(user));
	
	size_t line_size = 100;
	char* line = malloc(line_size);
	if(!line) {
		exit(EXIT_FAILURE);
	}
	
	/* Get the user's name */
	printf("Enter your first name:\n[>] ");
	strncpy(user.firstName, read_line(line, line_size), sizeof(user.firstName));
	
	printf("\nEnter your last name:\n[>] ");
	strncpy(user.lastName, read_line(line, line_size), sizeof(user.lastName));
	
	/* Greet the user */
	printf("\nHello, %s %s!\n\n", user.firstName, user.lastName);
	
	/* Get the user's age */
	printf("Enter your age:\n[>] ");
	scanf("%d", &user.age);
	if(user.age < 0) {
		printf("\nSince you're not born yet, you don't need to worry about grades!\n");
		return 0;
	}
	
	/* Scare the user */
	printf("In 5 years you will be %d years old!\n\n", user.age + 5);
	
	printf("On a scale of 1-10, how well did you do on your last math test?\n[>] ");
	unsigned score;
	scanf("%u", &score);
	
	/* Convert the user's score to a letter grade */
	switch(score) {
		case 0:
			printf("No wonder you failed at math.\n");
			return 0;
		
		case 1:
			strcpy(user.grade, "Z");
			break;
		
		case 2:
			strcpy(user.grade, "F");
			break;
			
		case 3:
			strcpy(user.grade, "D");
			break;
			
		case 4:
			strcpy(user.grade, "C");
			break;
			
		case 5:
			strcpy(user.grade, "B");
			break;
			
		case 6:
			strcpy(user.grade, "B+");
			break;
			
		case 7:
			strcpy(user.grade, "A-");
			break;
			
		default:
			/* Output A with 0 or more plusses, depending on the score */
			strncpy(user.grade, "A+++", MIN(sizeof(user.grade), score - 7));
			break;
	}
	
	/* Give the user their grade! */
	printf("\nHere's your math test back:\n");
	printf(user.grade);
	
	/* Don't be rude. Say goodbye! */
	printf("\n\nGoodbye!\n");
	free(line);
	
	return 0;
}
