under Problem {
  Type = UnsteadyAeroelastic;
  Framework = Embedded;
  Mode = Dimensional;  
}

under Input {
  GeometryPrefix = "../data/fluidmodel";
  
  Matcher = "../data/fluidmodel.match.fluid";
  EmbeddedSurface = "../sources/embeddedSurf.top";
  Solution = "references.Steady/Solution.bin";
}

under Output {
  under Postpro {
    Prefix = "results.FSI/";
    LiftandDrag = "../postpro.FSI/LiftandDrag.out";
    Force = "../postpro.FSI/Force.out";
    Mach = "Mach.bin";
    Pressure = "Pressure.bin";
    EmbeddedSurfaceDisplacement = "../postpro.Steady/EmbeddedSurfaceDisplacement.xpost";
    EmbeddedSurfacePressureCoefficient = "../postpro.Steady/EmbeddedSurfacePressureCoefficient.xpost";
    Frequency = 100;
    PostprocessSides = 1;
  }
  under Restart {
    Prefix = "references.FSI/"; 
    Solution = "Solution.bin";
    RestartData = "Restart.data";
    Position = "Position.data";
    EmbeddedPosition = "EmbeddedPosition.data";
    Frequency = 0;
  }

}

under Equations {
  Type = Euler;
  under FluidModel[0]{
    Fluid = PerfectGas;
  }
}

under BoundaryConditions {
  under Inlet {
    Mach = 0.97;
    Alpha = 7.5; 
    Beta = 0.0;
    Density = 0.61115933E-7;  // slugs / in^3
    Pressure = 6.0;           // psi*12 ([slugs/(in-s^2)])
  }
}

under Space {
  under NavierStokes { 
    Flux = Roe;
    Reconstruction = Linear;
    Limiter = VanAlbada;
    Gradient = LeastSquares;
    Beta = 0.333333333333333;
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
      FailSafe = AlwaysOn;
      under LinearSolver {
        under NavierStokes {
          Type = Gmres;
          MaxIts = 100;
          KrylovVectors = 100;
          Eps = 1.0e-4;
          //Output = "stdout";
          under Preconditioner { 
            Type = Ras; 
            Fill = 0; 
          }
        }
      }
    }
  }
}


under EmbeddedFramework {
  TypeHalfRiemannProblem = Surrogate;
  RiemannNormal = Structure;  
}

