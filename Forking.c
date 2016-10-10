#include <stdio.h>
#include <unistd.h> 
#include <stdlib.h>


int main (int argc, char **argv)
{
	int a = 0;
	int b = 0;
	int c = 0; 
	int d = 0; 
	int x = 1; 
	int y = 2; 
	int z = 3; 
	

	int pid = fork(); 
	if (pid == 0) 
	{		
		a = x + y;  
		printf("Child Process cries like a baby.\n");
		wait(0); 

	}
	else 
	{
		b = z + 1; 
		printf("Parent Process does parenting.\n"); 			exit(0); 

		
	}
	 c = a + b; 
	 d = c - 1; 

	 	printf("a = %d\nb = %d\nc = %d\nd = %d\nx = %d\ny = %d\nz = %d\n", a, b, c, d, x, y, z); 

}
