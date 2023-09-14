import React, { useState, useRef,useEffect } from 'react';
import * as d3 from 'd3';
import mermaid from 'mermaid';
import SideNav from './sidenav';
import { Box } from '@mui/material';
import './arrowCSS.css'

import mermaidAPI from 'mermaid'



export default function MermaidDiagram({mermaidCode}){
    useEffect(() => {
        mermaid.initialize({ startOnLoad: true ,theme : 'dark' });
        // mermaidAPI.initialize({theme : 'dark'})
        mermaid.contentLoaded()
        
      });
      console.log(mermaidCode);

// const mermaidCode = "classDiagram\n  class InputParameters {\n    + inputDate: string\n    + adjustDays: int\n    + adjustMonths: int \n    + adjustYears: int\n    + inputFormat: string\n    + outputFormat: string \n  }\n  \n  class DateUtilities {\n    + convertStringToDate(string, format): Date\n    + convertDateToString(date, format): string\n    + addDays(date, days): Date\n    + addMonths(date, months): Date\n    + addYears(date, years): Date\n  }\n  \n  class Main {\n    + main()\n    + sendErrorMessage(message): void\n  }\n  \n  InputParameters --> DateUtilities\n  DateUtilities --> Main\n  Main ..> InputParameters : uses"

//       const mermaidCode = `
//       classDiagram
//   class Animal {
//     +int age
//     +String gender
//     +isMammal()
//     +mate()
//   }

//   class Duck {
//     +String beakColor
//     +swim()
//     +quack()
//   }

//   class Fish {
//     -int sizeInFeet
//     -canEat()
//   }

//   class Zebra {
//     +bool is_wild
//     +run()
//   }

//   Animal <|-- Duck
//   Animal <|-- Fish
//   Animal <|-- Zebra

 

//     `;
   
    
    return(
        <>
            
            
            <div className="mermaid" dangerouslySetInnerHTML={{ __html: mermaidCode }} />
         
            
        </>
    )
}
