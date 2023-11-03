import React, { useState } from 'react';
import { Box, Button, Container } from '@mui/material';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import { styled } from '@mui/system';


const AnimatedBox = styled(Box)(({ theme, isExpanded }) => ({
  height: '52vw',
  width: isExpanded ? '40%' : '20%',
  transition: 'width 0.3s ease',
  borderRadius: '8px',
  boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.1)',
  backgroundColor: '#FFFFFF',
}));

const RoundedBox = styled(Box)({
  height: '52vw',
  borderRadius: '8px',
  boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.1)',
  backgroundColor: '#FFFFFF',
});

const FileDropBox = styled(Box)({
    display: 'flex',
    textAlign: 'left',
    fontSize:12,
    justifyContent: 'left',
    alignItems: 'flex-start', 
    height: '100%',
    border: '2px dashed #cccccc',
    borderRadius: '8px',
    backgroundColor: '#f9f9f9',
    padding: '8px',
    overflow: 'auto',
    whiteSpace: 'pre-wrap',
  });
  


export default function CodeBlock() {
  const [isExpandedBox1, setExpandedBox1] = useState(true);
  const [isExpandedBox3, setExpandedBox3] = useState(false);
  const [fileContent, setFileContent] = useState('');

  const handleBox1Click = () => {
    setExpandedBox1(true);
    setExpandedBox3(false);
  };

  const handleBox3Click = () => {
    setExpandedBox3(true);
    setExpandedBox1(false);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    const reader = new FileReader();

    reader.onload = () => {
      const content = reader.result;
      setFileContent(content);
    };

    reader.readAsText(file);
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  return (
    <Container sx={{ padding: '0px 0px 0px 0px', margin: '0px 0px 0px 0px' }}>
      <Box display="flex" justifyContent={'space-between'} width={'110%'} sx={{ padding: '0px', margin: '0px' , marginLeft:'200px' }}>

        <AnimatedBox  isExpanded={isExpandedBox1} onClick={handleBox1Click}>
          <FileDropBox

            
            onDrop={handleDrop}
            onDragOver={handleDragOver}
          >
            {fileContent ? (
              <p>{fileContent}</p>
            ) : (
              <p >Drag and drop a file here</p>
            )}
          </FileDropBox>
        </AnimatedBox>

        <Box display="flex"   alignItems="center">
          <ArrowForwardIcon />
        </Box>
         
          
        <RoundedBox width="60%" marginTop={'60px'}>
        <div class='flex justify-between mt-[-50px] bg-gray-400 p-1 ml-4 mr-4'>
          
        <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 border border-blue-700 rounded">
            Button
          </button>
          
          <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 border border-blue-700 rounded">
            Button
          </button>
          <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 border border-blue-700 rounded">
          Button
        </button>
          </div>
          <Box p={2} className="bg-white ">
          <div className='flex justify-between '>
            {/* <p class='bg-sky-500/100'>Nav1</p>
            <p class='bg-sky-500/100'>Nav2</p>
            <p class='bg-sky-500/100'>Nav3</p> */}

            </div>
          </Box>
        </RoundedBox>

       

        {/* <Box display="flex" alignItems="center">
          <ArrowForwardIcon />
        </Box> */}
        {/* <AnimatedBox isExpanded={isExpandedBox3} onClick={handleBox3Click}>
          <Box p={2} className="bg-white">
            <p>Box 3 Text</p>
          </Box>
        </AnimatedBox> */}
      </Box>
    </Container>
  );
}
