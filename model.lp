\* Source Pyomo model name=Model *\

min 
objective:
+10 InvestmentFlow_invest(_Reservoir__0x7ff58bf93458___Bus__0x7ff5b02d1688_)
+0.10000000000000001 flow(_Dispatchable__0x7ff580ea9598___Bus__0x7ff5b02d1688__0)
+5 flow(_Dispatchable__0x7ff580ea9598___Bus__0x7ff5b02d1688__1)
+100 flow(_Dispatchable__0x7ff580ea9598___Bus__0x7ff5b02d1688__2)

s.t.

c_e_Bus_balance(_Bus__0x7ff58bf7ff48__0)_:
-1 flow(_Bus__0x7ff58bf7ff48___Connection__0x7ff580e51598__0)
-1 flow(_Bus__0x7ff58bf7ff48___Conversion__0x7ff580e50d68__0)
-1 flow(_Bus__0x7ff58bf7ff48___Storage__0x7ff580ea9c78__0)
+1 flow(_Connection__0x7ff580e51598___Bus__0x7ff58bf7ff48__0)
+1 flow(_Storage__0x7ff580ea9c78___Bus__0x7ff58bf7ff48__0)
= 0

c_e_Bus_balance(_Bus__0x7ff58bf7ff48__1)_:
-1 flow(_Bus__0x7ff58bf7ff48___Connection__0x7ff580e51598__1)
-1 flow(_Bus__0x7ff58bf7ff48___Conversion__0x7ff580e50d68__1)
-1 flow(_Bus__0x7ff58bf7ff48___Storage__0x7ff580ea9c78__1)
+1 flow(_Connection__0x7ff580e51598___Bus__0x7ff58bf7ff48__1)
+1 flow(_Storage__0x7ff580ea9c78___Bus__0x7ff58bf7ff48__1)
= 0

c_e_Bus_balance(_Bus__0x7ff58bf7ff48__2)_:
-1 flow(_Bus__0x7ff58bf7ff48___Connection__0x7ff580e51598__2)
-1 flow(_Bus__0x7ff58bf7ff48___Conversion__0x7ff580e50d68__2)
-1 flow(_Bus__0x7ff58bf7ff48___Storage__0x7ff580ea9c78__2)
+1 flow(_Connection__0x7ff580e51598___Bus__0x7ff58bf7ff48__2)
+1 flow(_Storage__0x7ff580ea9c78___Bus__0x7ff58bf7ff48__2)
= 0

c_e_Bus_balance(_Bus__0x7ff58bf7ff98__0)_:
+1 flow(_BackpressureTurbine__0x7ff580ebf6d8___Bus__0x7ff58bf7ff98__0)
+1 flow(_Conversion__0x7ff580e50d68___Bus__0x7ff58bf7ff98__0)
= 0

c_e_Bus_balance(_Bus__0x7ff58bf7ff98__1)_:
+1 flow(_BackpressureTurbine__0x7ff580ebf6d8___Bus__0x7ff58bf7ff98__1)
+1 flow(_Conversion__0x7ff580e50d68___Bus__0x7ff58bf7ff98__1)
= 0

c_e_Bus_balance(_Bus__0x7ff58bf7ff98__2)_:
+1 flow(_BackpressureTurbine__0x7ff580ebf6d8___Bus__0x7ff58bf7ff98__2)
+1 flow(_Conversion__0x7ff580e50d68___Bus__0x7ff58bf7ff98__2)
= 0

c_e_Bus_balance(_Bus__0x7ff5b02d1688__0)_:
+1 flow(_BackpressureTurbine__0x7ff580ebf6d8___Bus__0x7ff5b02d1688__0)
-1 flow(_Bus__0x7ff5b02d1688___Connection__0x7ff580e51598__0)
+1 flow(_Connection__0x7ff580e51598___Bus__0x7ff5b02d1688__0)
+1 flow(_Dispatchable__0x7ff580ea9598___Bus__0x7ff5b02d1688__0)
+1 flow(_Reservoir__0x7ff58bf93458___Bus__0x7ff5b02d1688__0)
= 4

c_e_Bus_balance(_Bus__0x7ff5b02d1688__1)_:
+1 flow(_BackpressureTurbine__0x7ff580ebf6d8___Bus__0x7ff5b02d1688__1)
-1 flow(_Bus__0x7ff5b02d1688___Connection__0x7ff580e51598__1)
+1 flow(_Connection__0x7ff580e51598___Bus__0x7ff5b02d1688__1)
+1 flow(_Dispatchable__0x7ff580ea9598___Bus__0x7ff5b02d1688__1)
+1 flow(_Reservoir__0x7ff58bf93458___Bus__0x7ff5b02d1688__1)
= -1.6599999999999999

c_e_Bus_balance(_Bus__0x7ff5b02d1688__2)_:
+1 flow(_BackpressureTurbine__0x7ff580ebf6d8___Bus__0x7ff5b02d1688__2)
-1 flow(_Bus__0x7ff5b02d1688___Connection__0x7ff580e51598__2)
+1 flow(_Connection__0x7ff580e51598___Bus__0x7ff5b02d1688__2)
+1 flow(_Dispatchable__0x7ff580ea9598___Bus__0x7ff5b02d1688__2)
+1 flow(_Reservoir__0x7ff58bf93458___Bus__0x7ff5b02d1688__2)
= 43.399999999999999

c_e_Bus_balance(reservoir_bus__Reservoir__0x7ff58bf93458__0)_:
-1 flow(reservoir_bus__Reservoir__0x7ff58bf93458___Reservoir__0x7ff58bf93458__0)
-1 flow(reservoir_bus__Reservoir__0x7ff58bf93458__spillage_Reservoir__0x7ff58bf93458__0)
= -1

c_e_Bus_balance(reservoir_bus__Reservoir__0x7ff58bf93458__1)_:
-1 flow(reservoir_bus__Reservoir__0x7ff58bf93458___Reservoir__0x7ff58bf93458__1)
-1 flow(reservoir_bus__Reservoir__0x7ff58bf93458__spillage_Reservoir__0x7ff58bf93458__1)
= -2

c_e_Bus_balance(reservoir_bus__Reservoir__0x7ff58bf93458__2)_:
-1 flow(reservoir_bus__Reservoir__0x7ff58bf93458___Reservoir__0x7ff58bf93458__2)
-1 flow(reservoir_bus__Reservoir__0x7ff58bf93458__spillage_Reservoir__0x7ff58bf93458__2)
= -3

c_e_Transformer_relation(_BackpressureTurbine__0x7ff580ebf6d8___Bus__0x7ff58bf933b8___Bus__0x7ff58bf7ff98__0)_:
-2.5 flow(_BackpressureTurbine__0x7ff580ebf6d8___Bus__0x7ff58bf7ff98__0)
+1 flow(_Bus__0x7ff58bf933b8___BackpressureTurbine__0x7ff580ebf6d8__0)
= 0

c_e_Transformer_relation(_BackpressureTurbine__0x7ff580ebf6d8___Bus__0x7ff58bf933b8___Bus__0x7ff58bf7ff98__1)_:
-2.5 flow(_BackpressureTurbine__0x7ff580ebf6d8___Bus__0x7ff58bf7ff98__1)
+1 flow(_Bus__0x7ff58bf933b8___BackpressureTurbine__0x7ff580ebf6d8__1)
= 0

c_e_Transformer_relation(_BackpressureTurbine__0x7ff580ebf6d8___Bus__0x7ff58bf933b8___Bus__0x7ff58bf7ff98__2)_:
-2.5 flow(_BackpressureTurbine__0x7ff580ebf6d8___Bus__0x7ff58bf7ff98__2)
+1 flow(_Bus__0x7ff58bf933b8___BackpressureTurbine__0x7ff580ebf6d8__2)
= 0

c_e_Transformer_relation(_BackpressureTurbine__0x7ff580ebf6d8___Bus__0x7ff58bf933b8___Bus__0x7ff5b02d1688__0)_:
-2.2727272727272729 flow(_BackpressureTurbine__0x7ff580ebf6d8___Bus__0x7ff5b02d1688__0)
+1 flow(_Bus__0x7ff58bf933b8___BackpressureTurbine__0x7ff580ebf6d8__0)
= 0

c_e_Transformer_relation(_BackpressureTurbine__0x7ff580ebf6d8___Bus__0x7ff58bf933b8___Bus__0x7ff5b02d1688__1)_:
-2.2727272727272729 flow(_BackpressureTurbine__0x7ff580ebf6d8___Bus__0x7ff5b02d1688__1)
+1 flow(_Bus__0x7ff58bf933b8___BackpressureTurbine__0x7ff580ebf6d8__1)
= 0

c_e_Transformer_relation(_BackpressureTurbine__0x7ff580ebf6d8___Bus__0x7ff58bf933b8___Bus__0x7ff5b02d1688__2)_:
-2.2727272727272729 flow(_BackpressureTurbine__0x7ff580ebf6d8___Bus__0x7ff5b02d1688__2)
+1 flow(_Bus__0x7ff58bf933b8___BackpressureTurbine__0x7ff580ebf6d8__2)
= 0

c_e_Transformer_relation(_Conversion__0x7ff580e50d68___Bus__0x7ff58bf7ff48___Bus__0x7ff58bf7ff98__0)_:
+1 flow(_Bus__0x7ff58bf7ff48___Conversion__0x7ff580e50d68__0)
-1.0526315789473684 flow(_Conversion__0x7ff580e50d68___Bus__0x7ff58bf7ff98__0)
= 0

c_e_Transformer_relation(_Conversion__0x7ff580e50d68___Bus__0x7ff58bf7ff48___Bus__0x7ff58bf7ff98__1)_:
+1 flow(_Bus__0x7ff58bf7ff48___Conversion__0x7ff580e50d68__1)
-1.0526315789473684 flow(_Conversion__0x7ff580e50d68___Bus__0x7ff58bf7ff98__1)
= 0

c_e_Transformer_relation(_Conversion__0x7ff580e50d68___Bus__0x7ff58bf7ff48___Bus__0x7ff58bf7ff98__2)_:
+1 flow(_Bus__0x7ff58bf7ff48___Conversion__0x7ff580e50d68__2)
-1.0526315789473684 flow(_Conversion__0x7ff580e50d68___Bus__0x7ff58bf7ff98__2)
= 0

c_u_InvestmentFlow_max(_Reservoir__0x7ff58bf93458___Bus__0x7ff5b02d1688__0)_:
-1 InvestmentFlow_invest(_Reservoir__0x7ff58bf93458___Bus__0x7ff5b02d1688_)
+1 flow(_Reservoir__0x7ff58bf93458___Bus__0x7ff5b02d1688__0)
<= 0

c_u_InvestmentFlow_max(_Reservoir__0x7ff58bf93458___Bus__0x7ff5b02d1688__1)_:
-1 InvestmentFlow_invest(_Reservoir__0x7ff58bf93458___Bus__0x7ff5b02d1688_)
+1 flow(_Reservoir__0x7ff58bf93458___Bus__0x7ff5b02d1688__1)
<= 0

c_u_InvestmentFlow_max(_Reservoir__0x7ff58bf93458___Bus__0x7ff5b02d1688__2)_:
-1 InvestmentFlow_invest(_Reservoir__0x7ff58bf93458___Bus__0x7ff5b02d1688_)
+1 flow(_Reservoir__0x7ff58bf93458___Bus__0x7ff5b02d1688__2)
<= 0

c_e_LinkBlock_relation(_Connection__0x7ff580e51598___Bus__0x7ff58bf7ff48___Bus__0x7ff5b02d1688__0)_:
-0.92999999999999994 flow(_Bus__0x7ff58bf7ff48___Connection__0x7ff580e51598__0)
+1 flow(_Connection__0x7ff580e51598___Bus__0x7ff5b02d1688__0)
= 0

c_e_LinkBlock_relation(_Connection__0x7ff580e51598___Bus__0x7ff58bf7ff48___Bus__0x7ff5b02d1688__1)_:
-0.92999999999999994 flow(_Bus__0x7ff58bf7ff48___Connection__0x7ff580e51598__1)
+1 flow(_Connection__0x7ff580e51598___Bus__0x7ff5b02d1688__1)
= 0

c_e_LinkBlock_relation(_Connection__0x7ff580e51598___Bus__0x7ff58bf7ff48___Bus__0x7ff5b02d1688__2)_:
-0.92999999999999994 flow(_Bus__0x7ff58bf7ff48___Connection__0x7ff580e51598__2)
+1 flow(_Connection__0x7ff580e51598___Bus__0x7ff5b02d1688__2)
= 0

c_e_LinkBlock_relation(_Connection__0x7ff580e51598___Bus__0x7ff5b02d1688___Bus__0x7ff58bf7ff48__0)_:
-0.92999999999999994 flow(_Bus__0x7ff5b02d1688___Connection__0x7ff580e51598__0)
+1 flow(_Connection__0x7ff580e51598___Bus__0x7ff58bf7ff48__0)
= 0

c_e_LinkBlock_relation(_Connection__0x7ff580e51598___Bus__0x7ff5b02d1688___Bus__0x7ff58bf7ff48__1)_:
-0.92999999999999994 flow(_Bus__0x7ff5b02d1688___Connection__0x7ff580e51598__1)
+1 flow(_Connection__0x7ff580e51598___Bus__0x7ff58bf7ff48__1)
= 0

c_e_LinkBlock_relation(_Connection__0x7ff580e51598___Bus__0x7ff5b02d1688___Bus__0x7ff58bf7ff48__2)_:
-0.92999999999999994 flow(_Bus__0x7ff5b02d1688___Connection__0x7ff580e51598__2)
+1 flow(_Connection__0x7ff580e51598___Bus__0x7ff58bf7ff48__2)
= 0

c_e_GenericStorageBlock_balance(_Reservoir__0x7ff58bf93458__0)_:
+1 GenericStorageBlock_capacity(_Reservoir__0x7ff58bf93458__0)
-1 GenericStorageBlock_capacity(_Reservoir__0x7ff58bf93458__2)
+1 flow(_Reservoir__0x7ff58bf93458___Bus__0x7ff5b02d1688__0)
-1 flow(reservoir_bus__Reservoir__0x7ff58bf93458___Reservoir__0x7ff58bf93458__0)
= 0

c_e_GenericStorageBlock_balance(_Reservoir__0x7ff58bf93458__1)_:
-1 GenericStorageBlock_capacity(_Reservoir__0x7ff58bf93458__0)
+1 GenericStorageBlock_capacity(_Reservoir__0x7ff58bf93458__1)
+1 flow(_Reservoir__0x7ff58bf93458___Bus__0x7ff5b02d1688__1)
-1 flow(reservoir_bus__Reservoir__0x7ff58bf93458___Reservoir__0x7ff58bf93458__1)
= 0

c_e_GenericStorageBlock_balance(_Reservoir__0x7ff58bf93458__2)_:
-1 GenericStorageBlock_capacity(_Reservoir__0x7ff58bf93458__1)
+1 GenericStorageBlock_capacity(_Reservoir__0x7ff58bf93458__2)
+1 flow(_Reservoir__0x7ff58bf93458___Bus__0x7ff5b02d1688__2)
-1 flow(reservoir_bus__Reservoir__0x7ff58bf93458___Reservoir__0x7ff58bf93458__2)
= 0

c_e_GenericStorageBlock_balance(_Storage__0x7ff580ea9c78__0)_:
+1 GenericStorageBlock_capacity(_Storage__0x7ff580ea9c78__0)
-1 GenericStorageBlock_capacity(_Storage__0x7ff580ea9c78__2)
-1 flow(_Bus__0x7ff58bf7ff48___Storage__0x7ff580ea9c78__0)
+1 flow(_Storage__0x7ff580ea9c78___Bus__0x7ff58bf7ff48__0)
= 0

c_e_GenericStorageBlock_balance(_Storage__0x7ff580ea9c78__1)_:
-1 GenericStorageBlock_capacity(_Storage__0x7ff580ea9c78__0)
+1 GenericStorageBlock_capacity(_Storage__0x7ff580ea9c78__1)
-1 flow(_Bus__0x7ff58bf7ff48___Storage__0x7ff580ea9c78__1)
+1 flow(_Storage__0x7ff580ea9c78___Bus__0x7ff58bf7ff48__1)
= 0

c_e_GenericStorageBlock_balance(_Storage__0x7ff580ea9c78__2)_:
-1 GenericStorageBlock_capacity(_Storage__0x7ff580ea9c78__1)
+1 GenericStorageBlock_capacity(_Storage__0x7ff580ea9c78__2)
-1 flow(_Bus__0x7ff58bf7ff48___Storage__0x7ff580ea9c78__2)
+1 flow(_Storage__0x7ff580ea9c78___Bus__0x7ff58bf7ff48__2)
= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(_BackpressureTurbine__0x7ff580ebf6d8___Bus__0x7ff58bf7ff98__0) <= +inf
   0 <= flow(_BackpressureTurbine__0x7ff580ebf6d8___Bus__0x7ff58bf7ff98__1) <= +inf
   0 <= flow(_BackpressureTurbine__0x7ff580ebf6d8___Bus__0x7ff58bf7ff98__2) <= +inf
   0 <= flow(_BackpressureTurbine__0x7ff580ebf6d8___Bus__0x7ff5b02d1688__0) <= 10
   0 <= flow(_BackpressureTurbine__0x7ff580ebf6d8___Bus__0x7ff5b02d1688__1) <= 10
   0 <= flow(_BackpressureTurbine__0x7ff580ebf6d8___Bus__0x7ff5b02d1688__2) <= 10
   0 <= flow(_Bus__0x7ff58bf7ff48___Connection__0x7ff580e51598__0) <= +inf
   0 <= flow(_Bus__0x7ff58bf7ff48___Connection__0x7ff580e51598__1) <= +inf
   0 <= flow(_Bus__0x7ff58bf7ff48___Connection__0x7ff580e51598__2) <= +inf
   0 <= flow(_Bus__0x7ff58bf7ff48___Conversion__0x7ff580e50d68__0) <= +inf
   0 <= flow(_Bus__0x7ff58bf7ff48___Conversion__0x7ff580e50d68__1) <= +inf
   0 <= flow(_Bus__0x7ff58bf7ff48___Conversion__0x7ff580e50d68__2) <= +inf
   0 <= flow(_Bus__0x7ff58bf7ff48___Storage__0x7ff580ea9c78__0) <= 1
   0 <= flow(_Bus__0x7ff58bf7ff48___Storage__0x7ff580ea9c78__1) <= 1
   0 <= flow(_Bus__0x7ff58bf7ff48___Storage__0x7ff580ea9c78__2) <= 1
   0 <= flow(_Bus__0x7ff58bf933b8___BackpressureTurbine__0x7ff580ebf6d8__0) <= +inf
   0 <= flow(_Bus__0x7ff58bf933b8___BackpressureTurbine__0x7ff580ebf6d8__1) <= +inf
   0 <= flow(_Bus__0x7ff58bf933b8___BackpressureTurbine__0x7ff580ebf6d8__2) <= +inf
   0 <= flow(_Bus__0x7ff5b02d1688___Connection__0x7ff580e51598__0) <= +inf
   0 <= flow(_Bus__0x7ff5b02d1688___Connection__0x7ff580e51598__1) <= +inf
   0 <= flow(_Bus__0x7ff5b02d1688___Connection__0x7ff580e51598__2) <= +inf
   0 <= flow(_Connection__0x7ff580e51598___Bus__0x7ff58bf7ff48__0) <= 100
   0 <= flow(_Connection__0x7ff580e51598___Bus__0x7ff58bf7ff48__1) <= 100
   0 <= flow(_Connection__0x7ff580e51598___Bus__0x7ff58bf7ff48__2) <= 100
   0 <= flow(_Connection__0x7ff580e51598___Bus__0x7ff5b02d1688__0) <= 100
   0 <= flow(_Connection__0x7ff580e51598___Bus__0x7ff5b02d1688__1) <= 100
   0 <= flow(_Connection__0x7ff580e51598___Bus__0x7ff5b02d1688__2) <= 100
   0 <= flow(_Conversion__0x7ff580e50d68___Bus__0x7ff58bf7ff98__0) <= 2
   0 <= flow(_Conversion__0x7ff580e50d68___Bus__0x7ff58bf7ff98__1) <= 2
   0 <= flow(_Conversion__0x7ff580e50d68___Bus__0x7ff58bf7ff98__2) <= 2
   0 <= flow(_Dispatchable__0x7ff580ea9598___Bus__0x7ff5b02d1688__0) <= 10
   0 <= flow(_Dispatchable__0x7ff580ea9598___Bus__0x7ff5b02d1688__1) <= 10
   0 <= flow(_Dispatchable__0x7ff580ea9598___Bus__0x7ff5b02d1688__2) <= 10
   0 <= flow(_Reservoir__0x7ff58bf93458___Bus__0x7ff5b02d1688__0) <= +inf
   0 <= flow(_Reservoir__0x7ff58bf93458___Bus__0x7ff5b02d1688__1) <= +inf
   0 <= flow(_Reservoir__0x7ff58bf93458___Bus__0x7ff5b02d1688__2) <= +inf
   0 <= flow(_Storage__0x7ff580ea9c78___Bus__0x7ff58bf7ff48__0) <= 1
   0 <= flow(_Storage__0x7ff580ea9c78___Bus__0x7ff58bf7ff48__1) <= 1
   0 <= flow(_Storage__0x7ff580ea9c78___Bus__0x7ff58bf7ff48__2) <= 1
   0 <= flow(reservoir_bus__Reservoir__0x7ff58bf93458___Reservoir__0x7ff58bf93458__0) <= +inf
   0 <= flow(reservoir_bus__Reservoir__0x7ff58bf93458___Reservoir__0x7ff58bf93458__1) <= +inf
   0 <= flow(reservoir_bus__Reservoir__0x7ff58bf93458___Reservoir__0x7ff58bf93458__2) <= +inf
   0 <= flow(reservoir_bus__Reservoir__0x7ff58bf93458__spillage_Reservoir__0x7ff58bf93458__0) <= +inf
   0 <= flow(reservoir_bus__Reservoir__0x7ff58bf93458__spillage_Reservoir__0x7ff58bf93458__1) <= +inf
   0 <= flow(reservoir_bus__Reservoir__0x7ff58bf93458__spillage_Reservoir__0x7ff58bf93458__2) <= +inf
   0 <= InvestmentFlow_invest(_Reservoir__0x7ff58bf93458___Bus__0x7ff5b02d1688_) <= +inf
   0 <= GenericStorageBlock_capacity(_Reservoir__0x7ff58bf93458__0) <= 100
   0 <= GenericStorageBlock_capacity(_Reservoir__0x7ff58bf93458__1) <= 100
   0 <= GenericStorageBlock_capacity(_Reservoir__0x7ff58bf93458__2) <= 100
   0 <= GenericStorageBlock_capacity(_Storage__0x7ff580ea9c78__0) <= 10
   0 <= GenericStorageBlock_capacity(_Storage__0x7ff580ea9c78__1) <= 10
   0 <= GenericStorageBlock_capacity(_Storage__0x7ff580ea9c78__2) <= 10
end
