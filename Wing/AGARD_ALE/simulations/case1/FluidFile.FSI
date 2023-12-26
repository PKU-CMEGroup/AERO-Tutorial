under Problem {
  Type = UnsteadyAeroelastic;
  Mode = Dimensional; 
  Framework = BodyFitted;
}

under Input {
  GeometryPrefix = "../../data/OUTPUT";
  Matcher = "../../data/OUTPUT.match";
  
  Solution = "references.Steady/Solution.bin";
  //RestartData = "references.Steady/Restart.data";
}

under Output {
  under Postpro {
    Frequency = 100;
    Prefix = "results.FSI/";
    LiftandDrag = "../postpro.Steady/LiftandDrag.out";
    Force = "../postpro.Steady/Force.out";
    Velocity = "Mach.bin";
    Pressure = "Pressure.bin"; 
  }
  under Restart {
    Frequency = 0;
    Prefix = "references.FSI/"; 
    Solution = "Solution.bin";
    RestartData = "Restart.data";
    Position = "Position.bin"; 
  }
}


under Equations {  
  Type = Euler;   
  under FluidModel[0] {
    Fluid = PerfectGas;
    under GasModel {
      SpecificHeatRatio = 1.4;
    }
  }
}

under BoundaryConditions {
  under Inlet {
    Mach = 0.97;
    Alpha = 0.0; 
    Beta = 0.0;
    Density = 0.61115933E-7;     // slugs / in^3
    Pressure = 6.0;              // psi*12 ([slugs/(in-s^2)])
  }
}

under Space {     
  under NavierStokes {
    Flux = Roe;
    Reconstruction = Linear;
    AdvectiveOperator = FiniteVolume;
    Limiter = VanAlbada;
    Gradient = LeastSquares;
    Dissipation = SecondOrder;
    Beta = 0.3333333333333333;
    Gamma = 1.0;
  }
  under Boundaries {
    Type = StegerWarming;
  }
}


under Time {
  Type = Implicit;
  MaxIts = 5000;
  under CflLaw {
     Cfl0 = 1.0e+2;
     CflMax = 1.0e+2;
  }
    
  under Implicit {
    //Type = ThreePointBackwardDifference;
    Type = RungeKutta2;
    MatrixVectorProduct = FiniteDifference;
    under Newton { 
      MaxIts = 5; 
      Eps = 1e-05;
      FailSafe = On;
      under LinearSolver {
        under NavierStokes {
          Type = Gmres;
          MaxIts = 100;
          KrylovVectors = 100;
          Eps = 1.0e-4;
          under Preconditioner { 
            Type = Ras; 
            Fill = 0; 
          }
        }
      }
    }
  }
}

