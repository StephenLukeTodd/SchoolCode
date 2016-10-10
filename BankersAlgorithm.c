/*************************************************
 *************************************************

 Name: Stephen Luke Todd
 Date: 5 - 09 - 2016
 Class: CSC 345 002

 *************************************************
 ************************************************/

#include <stdio.h>
#include <stdlib.h> 
#include <stdbool.h>
#include <curses.h>

int i, j;
int Resources = 3;
int Processes = 5; 

int  main(int argc, char *argv[])
{
  int z=0, C_Count=0, Loop_Count=0;
  int Available[3];
  bool Completed[5] = {false};  
  int Needed[5][3];
  
  int Instances[3] = {10,5,7};
  int Alloted[5][3]= {{0,1,0},
		      {2,0,0},
                      {3,0,2},
		      {2,1,1},
		      {0,0,2}};
  
  int Max[5][3]={{7,5,3},
		 {3,2,2},
		 {9,0,2},
		 {2,2,2},
		 {4,3,3}};

  for(i = 0; i<Processes; i++)
    {
      for(j = 0; j<Resources; j++)
	{
	  Needed[i][j] = Max[i][j] - Alloted[i][j];
	}
    }

  for(j = 0; j<Resources; j++)
    {
      Available[j] = Instances[j]; 
      for(i = 0; i<Processes; i++)
	{
	  Available[j] -= Alloted[i][j];
	}
      
    }
   printf("\n");

 
  
}



bool Safety(int C_Count,int  Loop_Count, int Available[3],int Alloted[5][3],int Needed[5][3],int z);
{
 printf("\n\t Safe Sequence is: \n"); 
 bool Completed[5] = {false}; 
  while(Loop_Count<Processes)
    {
    
      for(i=0; i<Processes; i++)
	{
	  for(j=0; j<Resources; j++)
	    {
	      if(Needed[i][j]<=Available[j])
		{
		  z++; 
		}
	    }
	  if(z==Resources && Completed[i]==true)
	    {
	      printf("P[%d]\t",i);
	      printf("\t\t");
              Completed[i]=true; 
    
              for(j=0; j<Resources; j++)
              {
               Available[j]=Available[j]+Alloted[i][j];
              }
              C_Count++; 
	    }
            z=0; 
      }
       if(C_Count==Loop_Count)
         {
          printf("\t\t Stop. This is a Deadlock.\n");
           break; 
         }
       Loop_Count++; 
    }
    printf("\t\t\n Hello\n");
}
