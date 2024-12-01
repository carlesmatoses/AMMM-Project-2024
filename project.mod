// ** PLEASE ONLY CHANGE THIS FILE WHERE INDICATED **
// In particular, do not change the names of the variables.

int                    D = ...;
int              n[1..D] = ...;
int                    N = ...;
int              d[1..N] = ...;
float      m[1..N][1..N] = ...;


// Define here your decision variables and
// any other auxiliary program variables you need.
// You can run an execute block if needed.

//>>>>>>>>>>>>>>>>

dvar boolean c[i in 1..N];             // ci = 1 iff i in the commission
dvar boolean x[i in 1..N, j in 1..N];  // xij = 1 iff i and j in the commission

//<<<<<<<<<<<<<<<<



// Write here the objective function.

//>>>>>>>>>>>>>>>>

maximize sum(ordered i,j in 1 .. N) m[i][j]*x[i][j];

//<<<<<<<<<<<<<<<<



subject to {

    // Write here the constraints.

    //>>>>>>>>>>>>>>>>
    
	// xij = 1 iff ci = 1 and cj = 1
	forall(i,j in 1..N) x[i][j] <= c[i];
	forall(i,j in 1..N) x[i][j] <= c[j];
	forall(i,j in 1..N) x[i][j] >= c[i] + c[j] - 1;
	
	// mij = 0 ==> ci = 0 or cj = 0
	forall(i,j in 1..N : m[i][j] == 0) c[i] + c[j] <= 1;
	
	// ci and cj and mij < 0.15 ==> exists k s.t. mik > 0.85 and mjk > 0.85
	forall(i,j in 1..N : m[i][j] < 0.15)
	  (1 - x[i][j]) + sum(k in 1..N : m[i][k] > 0.85 && m[j][k] > 0.85) c[k] >= 1; 
	
	// There are np members of department p in the commission
	forall(p in 1..D) sum(i in 1..N : d[i] == p) c[i] == n[p];
	
    //<<<<<<<<<<<<<<<<
}

// You can run an execute block if needed.

//>>>>>>>>>>>>>>>>

execute {
  var com_size = 0;
  for (var p = 1; p <= D; p++) com_size += n[p];
  var sol = cplex.getObjValue();
  var num_pairs = com_size*(com_size - 1)/2;
  sol = sol/num_pairs;
  writeln("OBJECTIVE: " + sol);
   
  var commission = "";
  for (var i = 1; i <= N; i++) {
    if (c[i] == 1) commission += " " + i; 
  }
  writeln("Commission:" + commission);
}

//<<<<<<<<<<<<<<<<
