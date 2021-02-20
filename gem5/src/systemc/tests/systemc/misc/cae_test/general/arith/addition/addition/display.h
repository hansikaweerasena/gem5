/*****************************************************************************

  Licensed to Accellera Systems Initiative Inc. (Accellera) under one or
  more contributor license agreements.  See the NOTICE file distributed
  with this work for additional information regarding copyright ownership.
  Accellera licenses this file to you under the Apache License, Version 2.0
  (the "License"); you may not use this file except in compliance with the
  License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
  implied.  See the License for the specific language governing
  permissions and limitations under the License.

 *****************************************************************************/

/*****************************************************************************

  display.h -- 

  Original Author: Rocco Jonack, Synopsys, Inc., 1999-05-12

 *****************************************************************************/

/*****************************************************************************

  MODIFICATION LOG - modifiers, enter your name, affiliation, date and
  changes you are making here.

      Name, Affiliation, Date:
  Description of Modification:

 *****************************************************************************/

#include "common.h"

SC_MODULE( display )
{
  SC_HAS_PROCESS( display );

  sc_in_clk clk;

  const sc_signal<int>&              in_data1;     // Input  port
  const sc_signal_bool_vector4&      in_data2;     // Input  port
  const sc_signal_bool_vector4&      in_data3;     // Input  port
  const sc_signal_bool_vector8&      in_data4;     // Input  port
  const sc_signal_bool_vector8&      in_data5;     // Input  port
  const sc_signal<bool>& in_valid;

  display( sc_module_name NAME,
	   sc_clock&   CLK,
	   const  sc_signal<int>&              IN_DATA1,
	   const  sc_signal_bool_vector4&      IN_DATA2,      
	   const  sc_signal_bool_vector4&      IN_DATA3,     
	   const  sc_signal_bool_vector8&      IN_DATA4,      
	   const  sc_signal_bool_vector8&      IN_DATA5,     
           const sc_signal<bool>&              IN_VALID
	   )
  : 
    in_data1(IN_DATA1),
    in_data2(IN_DATA2),
    in_data3(IN_DATA3),
    in_data4(IN_DATA4),
    in_data5(IN_DATA5),
    in_valid(IN_VALID)
  {
    clk(CLK);
	SC_CTHREAD( entry, clk.pos() );
  }

  void entry();
};

// EOF
