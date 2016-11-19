//============================================================================
// Name        : Stephen Luke Todd
// Author      : *The name above this one*
// Date        : Who knows 
//****************************************************************************



#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <stdbool.h>
#include <fcntl.h>
#define BUFFER_SIZE 129
#define CMD_SIZE 15

char *path;
char *cwd;
char *args[CMD_SIZE];
pid_t pid;
int status;
int Parser(char *str);
bool SpecialTumblrSnowflake(int n);
bool DefaultFeature(int tCount);
void EXEBuiltIn(int tCount);
void EXEDayOneDLC(int tCount);

int main(void)
{
	// Declares path and CWD variables.
	path = getenv("PATH");
	cwd = getenv("PWD");
	char buffer[BUFFER_SIZE];


	while(true)
	{
		int tokenCount = 0;
		char line[BUFFER_SIZE];

		int i = 0;
		while(i < CMD_SIZE)	// Empties clear and argument.
		{
			args[i] = '\0';
			i++;
		}

		//It prints out a new header on a new line, including the current directory.  
		printf("myshell %s $", getcwd(buffer[BUFFER_SIZE], BUFFER_SIZE));
		fgets(line, BUFFER_SIZE, stdin);

		//Parses arguments inputted by said user.
		tokenCount = Parser(line);

		//Any arguments inputted made are put through. 
		if(tokenCount > 0)
		{
			//If the command is built in, then run it. 
			if(DefaultFeature(tokenCount))
				EXEBuiltIn(tokenCount);
			else
			        EXEDayOneDLC(tokenCount);
		}

	}
	**args = 0;
	return 0;
}

int Parser(char *str)
{
	char *curr = str;
	char *end = str;
	int charCount = 0;
	int tokenCount = 0;

	while(*end != '\0')
	{
		switch(*end)
		{
			//When you have whitespace. 
			case ' ':
			case '\n':
			case '\0':
			case '\t':
				if(charCount == 0)		//If there was no text before this, then ignore it. 
				{
					end++;
					curr++;
				}
				else				//Count the text as a token and store some pointer to the beginning of said token in args[]. 
				{
					tokenCount++;					//Increment by one the token counter. 
					*end = '\0';					//Set white space to 0 to signify end of it. 
					args[tokenCount - 1] = curr;		//Add previous token to args[].
					end++;							//Continue moving forward to the next index of the array. 
					curr = end;
					charCount = 0;					//Reset the character count so it can be recycled. 
				}
				break;

			case '>':
				end--;				// Checks the previous command to see if you aren't acquiring other methods when not needed.
				if(*end != ' ' && *end != '\0' && *end != '\n' && *end != '\t')		//For no spaces. 
				{
					end++;							//Go back to the original value. 
					tokenCount++;					//Increament the token counterer by 1 at a time.
					*end = '\0';					//Set the > operand and 0 to fix the no space issue. 
					args[tokenCount - 1] = curr;		//Put in the previous token to args[]
				}
				else
					end++;
				end++;							//Move onto the next index in said array. 
				curr = end;
				charCount = 0;					//Reset the character count so you can recycle it. 
				//Fix any issue created by overwriting the > operand.
				if(*end == '>')			//If so add a concatenate token and continue Check to see if said item is at the next index is also the > operand. 
				{
					printf("Concatenation redirection is not supported in the current version of this shell.\n");
					return 0;
				}
				else
				{
					tokenCount++;
					args[tokenCount - 1] = ">";
//					printf("Found a \'%s\'.\n", args[tokenCount - 1]);
				}
				break;

			case '<':
				end--;				//Check the previous int to make sure another command isn't being acquired illegally.
				if(*end != ' ' && *end != '\0' && *end != '\n' && *end != '\t')		//If there isn't a space.
				{
					end++;							//Go back to the original value for the end. 
					tokenCount++;					//Increment the token counter one at a time.
					*end = '\0';					//Set the < oeperand to 0 to fix any no space issue.
					args[tokenCount - 1] = curr;		// Put previous token to args[].
				}
				else
					end++;
				end++;							// continue traversing the line at the next index Move onto the next index. 
				curr = end;
				charCount = 0;					// Reset the character count to zero. 

				// Fix issue created by overwriting the < operand. 
				tokenCount++;
				args[tokenCount - 1] = "<";
//				printf("Found a \'%s\'.\n", args[tokenCount - 1]);
				break;

			case ';':
			case '|':
			case '&':
			case '$':
			case '"':
			case '\'':
				end++;
				*end = '\0';
				end--;
				printf("%s\'s are not supported in this version of the shell.\n", end);
				return 0;
				break;
			default:
				end++;
				charCount++;
		}
	}

	//Parse the last command after said loop closes.
	if(charCount > 0)
	{
		tokenCount++;
		args[tokenCount - 1] = curr;
		*end = '\0';
	}
	return tokenCount;
}

bool DefaultFeature(int tCount)
{
	int i = 0;
	// check to see if there are any special symbols. If so, treat the command like a non-built-in command Check to see if there any special snowflake symbols. In the case there is, treat command like a nonbuiltin command.
	while(i < tCount)
	{
		if(SpecialTumblrSnowflake(i))
			return false;
		i++;
	}
	//Return whether or not the command is a built-in. 
	// if statement works because 0 is considered false, and strcmp() returns 0 if there are no differences
	if(!strcmp(args[0], "cd") || !strcmp(args[0], "pwd") || !strcmp(args[0], "exit"))
		return true;
	return false;
}

void EXEBuiltIn(int tCount)
{
	//Run the command associated with this.
	char bufferCommand[BUFFER_SIZE];
	if(!strcmp(args[0], "cd"))
	{
		if(chdir(args[1]))
			printf("Command failed (cd). Invalid directory.\n");
	}

	else if(!strcmp(args[0], "pwd"))
	{
		char* pwd = getcwd(bufferCommand, BUFFER_SIZE);
		printf("%s\n", pwd);
	}

	else
	{
		printf("Exiting techshell.\n");
		exit(0);
	}
}

bool SpecialTumblrSnowflake(int n)
{
	if(*args[n] == '<' || *args[n] == '>')	//Checks to see if the token is a special snowflake. 
		return true;
	return false;
}

void EXEDayOneDLC(int tCount)
{
	char *cmd[CMD_SIZE];
	int i = 0;
	while(i < CMD_SIZE)	//  Sets cmd[] to null character in order to get around random mem leftovers. 
	{
		cmd[i] = '\0';
		i++;
	}
	
	i = 0;
	while(i < tCount)
	{
		if(!SpecialTumblrSnowflake(i))
		{
			cmd[i] = args[i];
		}
		else
			break;
		i++;
	}

	//Makes a new process.
	pid = fork();

	// If the Parent ID is -, then show that the fork failed.
	if(pid < 0)
	{
		printf("Fork failed.\n");
		exit(-1);
	}
	//If the parent ID is zero, run the new process.
	else if (pid == 0)
	{
		int fdOut, fdIn;
		while(i < tCount)
		{
			if(*args[i] == '>')		//If > operand, output to file. 
			{
				if((i + 2) > tCount)
				{
					printf("A filename must be provided in order for redirection to occur.\n");
					exit(0);
				}
				else if((i + 2) < tCount)
				{
					printf("Only 1 command and 1 redirection are allowed per line.\n");
					exit(0);
				}
				i++;
				fdOut = open(args[i], O_CREAT | O_WRONLY | O_TRUNC, 0666);
			     dup2(fdOut, STDOUT_FILENO);
				close(fdOut);
				i++;
				break;
			}
			else if(*args[i] == '<')	//If not, if < operand is found, that the file as input from the keyboard. 
			{
				if((i + 2) > tCount)
				{
					printf("A filename must be provided in order for redirection to occur.\n");
					exit(0);
				}
				else if((i + 2) < tCount)
				{
					printf("Only 1 command and 1 redirection are allowed per line.\n");
					exit(0);
				}
				i++;
				fdIn = open(args[i], O_RDONLY, 0666);
				dup2(fdIn, STDIN_FILENO);
				close(fdIn);
				break;
			}
			else					//If else, go to next token. 
				i++;
		}

		execvp(cmd[0], cmd);
		exit(0);
	}
	//For the parent process. 
	else
	{
		wait(NULL);
	}
}


