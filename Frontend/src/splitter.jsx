import { useState, useEffect } from 'react';
import * as React from 'react';
import PropTypes from 'prop-types';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Box from '@mui/material/Box';
import useAppStore from './assets/components/states';
import { Button, Divider, Drawer, Fab, IconButton } from '@mui/material';
import { Split } from "@geoffcox/react-splitter";
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Download, Edit, ReplayOutlined, Save } from '@mui/icons-material';
import './splitter.css'
import mermaid from 'mermaid';
import MermaidDiagram from './assets/components/mermaid';
import AceEditor from "react-ace";
import { saveAs } from 'file-saver';

import "ace-builds/src-noconflict/mode-python";
import "ace-builds/src-noconflict/theme-clouds_midnight";
import "ace-builds/src-noconflict/ext-language_tools"
import CircularProgress from '@mui/material/CircularProgress';







const RPGLECodeBlock = ({ fileContent }) => {

    const codeStyles = {
        comment: { color: '#999' },
        string: { color: '#d9d9d9' },
        keyword: { color: '#f00' },
        operator: { color: '#008000' },
        number: { color: '#9d38bd' },
        punctuation: { color: '#999' },
        datatype: { color: '#87CEEB' }
    };

    const language = {
        comment: {
            pattern: /\/\/.*|\/\*[\s\S]*?\*\//g,
            greedy: true,
        },
        string: /'(?:[^'\\]|\\.)*'|"(?:[^"\\]|\\.)*"/g,
        number: /\b\d+(?:\.\d+)?\b/g,
        keyword: /\b(?:ctl-opt|DCL|dcl-c|dcl-ds|dcl-f|dcl-pr|end-ds|dcl-pi|dcl-proc|dcl-s|dow|dou|doweq|doueq|dowlt|doult|dowle|doule|dowgt|dougt|dowge|douge|if|elseif|else|endif|end-pi|select|when|other|endsl|monitor|on-error|endmon|return|end-proc|end-pr|eval|call|exsr|chain|read|setll|setgt|reade|readp|chain(e)|read(e)|setll(e)|setgt(e)|reade(e)|readp(e)|write|update|delete|doune|enddo|DCL|DCLF|RCVF|PRTLN|MONMSG|CHGVAR|GOTO|ENDPGM)\b/gi,
        datatype: /\b(?:char|date|time|packed|zoned|integer|numeric|dec|float)\b/gi,
        operator: /[-+*/%=&<>]/g,
        punctuation: /[\(\)\[\]\{\},;]/g,
    };


    return (
        <SyntaxHighlighter showLineNumbers language={language} style={vscDarkPlus} customStyle={{ codeStyles, height: '96.5%', borderRadius: '15px' }}>
            {fileContent?fileContent:''}
        </SyntaxHighlighter>
     
    );
};
const LogicBlock = ({ businessLogic }) => {
    return (
        <div className='vscDarkPre vscDark' style={{ width: '100%', height: '93%', borderRadius: '15px' }}>
            {businessLogic}
        </div>
    );
};

const renderSplitter = (props) => {
    return <div className="w-2 h-full" style={{ backgroundColor: '#535F7E' }}></div>
};

function CustomTabPanel(props) {
    const { children, value, index, ...other } = props;


    return (
        <div
            className='h-full'
            role="tabpanel"
            hidden={value !== index}
            id={`simple-tabpanel-${index}`}
            aria-labelledby={`simple-tab-${index}`}
            {...other}
        >
            {value === index && (
                <Box sx={{ height: '100%' }}>
                    {children}
                </Box>
            )}
        </div>
    );
}
CustomTabPanel.propTypes = {
    children: PropTypes.node,
    index: PropTypes.number.isRequired,
    value: PropTypes.number.isRequired,
};
function a11yProps(index) {
    return {
        id: `simple-tab-${index}`,
        'aria-controls': `simple-tabpanel-${index}`,
    };
}

const useStyles = {
    editor: {
        border: '1px solid #ccc',
        overflow: 'auto',
    },
    result: {
        border: '1px solid #ccc',
        overflow: 'auto',
        background: '#f8f8f8',
        // width: '19%'

    },
};
export default function InteractiveArea() {

   

    const [logicLoader, setLogicLoader] = useState(false)
    const [diagramLoader, setDiagramLoader] = useState(false)
    const [javaLoader, setJavaLoader] = useState(false)

    const fileContent = useAppStore((state) => state.fileContent);
    const selectedFileID = useAppStore((state) => state.selectedFileID);
    const fileName = useAppStore((state) => state.fileName)
    const [selectedLogicID, setSelectedLogicID] = useState(null);
    const isGenButtonClicked = useAppStore((state) => state.isGenButtonClicked);
    const setIsGenButtonClicked = useAppStore((state)=>state.setIsGenButtonClicked)
    const [value, setValue] = useState(0);
    const [merm, setMerm] = useState(false);

    const [isEditing, setIsEditing] = useState(false);
    const [businessLogic, setBusinessLogic] = useState('');
    const [flowchartCode, setFlowchartCode] = useState('')
    const [classDiagramCode, setClassDiagramCode] = useState('')
    const [javaCode, setJavaCode] = useState('');

    useEffect(() => {

        mermaid.initialize({
            startOnLoad: true,
        });
        mermaid.contentLoaded()
    }, [value]);
    useEffect(() => {
        mermaid.contentLoaded()
    }, [flowchartCode, classDiagramCode]);

    const handleEditClick = () => {
        setIsEditing(true);
    };
    function onChange(newValue) {
        setJavaCode(newValue)
        console.log("change", newValue);
    }
    const handleInputChange = (e) => {
        setBusinessLogic(e.target.value);
    };

    const handleSaveClick = async (id) => {
        setIsEditing(false);
        setLogicLoader(true)
        setDiagramLoader(true)
        const jwtToken = sessionStorage.getItem("jwt");
        try {
            const genratedResponse = await fetch(`http://127.0.0.1:8000/logic/${selectedFileID}/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${jwtToken}`,
                },
                body: JSON.stringify({ 'logic': businessLogic })
            });
            const dataGen = await genratedResponse.json();
            setBusinessLogic(dataGen.logic)
            setSelectedLogicID(dataGen.id)
            generateMermaidDiagramsNew(dataGen.id)
            generateJavaCodeNew(dataGen.id)
            setLogicLoader(false)
        } catch(error) {
            console.log(error)
        }
    };
    const handleDownload = (fileType) => {
        let extractedValue = '';
        if (fileName) {
            const dotIndex = fileName.lastIndexOf('.');
        if (dotIndex !== -1) {
            extractedValue = fileName.substring(0, dotIndex);
        }
        }

        switch (fileType) {
            case 'mmd':
                // const mmdContent1 = 'MMD File 1 content';
                // const mmdContent2 = 'MMD File 2 content';

                const blob1 = new Blob([flowchartCode], { type: 'text/plain;charset=utf-8' });
                const blob2 = new Blob([classDiagramCode], { type: 'text/plain;charset=utf-8' });

                saveAs(blob1, `${extractedValue}_flowchart.mmd`);
                saveAs(blob2, `${extractedValue}_classdiagram.mmd`);
                break;

            case 'java':

                const blob = new Blob([javaCode], { type: 'text/plain;charset=utf-8' });
                saveAs(blob,`${extractedValue}.py`);
                break;

            default:
                return;
        }
    };

    const handleChange = (event, newValue) => {
        setValue(newValue);
        mermaid.contentLoaded()
        setMerm(!merm)
    };

    const generateMermaidDiagrams = async (id) => {
        setDiagramLoader(true)
        const jwtToken = sessionStorage.getItem("jwt");
        try {
            const response = await fetch(`http://127.0.0.1:8000/mermaid/${selectedFileID}/${id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${jwtToken}`,
                },
            })
            const data = await response.json();
            console.log(data)
            mermaid.contentLoaded()
            setFlowchartCode(data.flowChart)
            setClassDiagramCode(data.classDiagram)
            setDiagramLoader(false)
            mermaid.contentLoaded()

        } catch(error) {
            console.log(error)
        }
    }
    const generateMermaidDiagramsNew = async (id) => {
        setDiagramLoader(true)
        const jwtToken = sessionStorage.getItem("jwt");
        try {
            const response = await fetch(`http://127.0.0.1:8000/mermaid/${selectedFileID}/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${jwtToken}`,
                },
            })
            const data = await response.json();
            console.log(data)
            mermaid.contentLoaded()
            setFlowchartCode(data.flowChart)
            setClassDiagramCode(data.classDiagram)
            setDiagramLoader(false)
            mermaid.contentLoaded()

        } catch(error) {
            console.log(error)
        }
    }

    const generateBusinessLogic = async () => {
        setIsGenButtonClicked(true)
        setLogicLoader(true)
        setDiagramLoader(true)
        setJavaLoader(true)
        const jwtToken = sessionStorage.getItem("jwt");
        try {
            const genratedResponse = await fetch(`http://127.0.0.1:8000/logic/${selectedFileID}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${jwtToken}`,
                },
            });
            const dataGen = await genratedResponse.json();
            setBusinessLogic(dataGen.logic)
            setSelectedLogicID(dataGen.id)
            generateMermaidDiagrams(dataGen.id)
            generateJavaCode(dataGen.id)
            setLogicLoader(false)
        } catch(error) {
            console.log(error)
        }

    };

    const generateJavaCode = async (id) => {
        setJavaLoader(true)
        const jwtToken = sessionStorage.getItem("jwt");
        try {
            const genratedResponse = await fetch(`http://127.0.0.1:8000/java/${selectedFileID}/${id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${jwtToken}`,
                },
            });
            const dataGen = await genratedResponse.json();
            setJavaCode(dataGen.code)
            setJavaLoader(false)
        } catch(error) {
            console.log(error)
        }

    };
    const generateJavaCodeNew = async (id) => {
        setJavaLoader(true)
        const jwtToken = sessionStorage.getItem("jwt");
        try {
            const genratedResponse = await fetch(`http://127.0.0.1:8000/java/${selectedFileID}/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${jwtToken}`,
                },
            });
            const dataGen = await genratedResponse.json();
            setJavaCode(dataGen.code)
            setJavaLoader(false)
        } catch(error) {
            console.log(error)
        }

    };

    return (
        <div
            className='w-full h-full'
        >

            <Split initialPrimarySize={(isGenButtonClicked)?"50%":"100%"} minPrimarySize="30%" renderSplitter={renderSplitter}>
                <div className='h-full' style={{
                    background: 'black'
                }}>
                    <div className='flex justify-center px-5'>
                        <div className='fileName' style={{
                            background: 'black'
                        }}>
                            <p style={{ color: '#1976d2', fontSize: '15px' }}>  {fileName} </p>
                        </div>
                    </div>
                    <div style={{ position: 'relative', width: '100%', height: '94.5%' }}>

                        <div
                            className=' overflow-y-scroll overflow-x-scroll rounded-xl'
                            style={{
                                background: 'black',
                                paddingTop: '20px',
                                paddingLeft: '15px',
                                paddingRight: '15px',
                                width: '100%',
                                height: '100%'

                            }}
                        >
                            <RPGLECodeBlock fileContent={fileContent} />
                        </div>
                        <div style={{ position: 'absolute', bottom: '32px', right: '25px' }}>
                            <div className='flex flex-col justify-center items-center' style={{
                                height: '7.5%',
                            }} >
                                <Button variant='outlined' sx={{ color: '#39FF14' }} onClick={() => { generateBusinessLogic() }} >Generate</Button>
                            </div>
                        </div>
                    </div>
                </div>
                <div className='h-full' style={{
                    background: 'black'
                }}>
                    <div style={{ height: '100%' }}>
                        <Box sx={{ borderBottom: 1, borderColor: 'divider', backgroundColor: '#000' }}>
                            <Tabs value={value} onChange={handleChange} aria-label="basic tabs example" sx={{ color: 'black', fontWeight: '600' }}>
                                <Tab sx={{ color: 'white' }} label="Business Logic" {...a11yProps(0)} />
                                <Tab sx={{ color: 'white' }} label="Mermaid Diagram" {...a11yProps(1)} />
                                <Tab sx={{ color: 'white' }} label="Python Code" {...a11yProps(2)} />
                            </Tabs>
                        </Box>


                        <CustomTabPanel value={value} index={0}>

                            <div style={{
                                height: '100%'
                            }} >

                                {
                                    (logicLoader) ? <>

                                        {<div className='flex h-full w-full justify-center items-center'  ><CircularProgress /></div>}
                                    </>
                                        :
                                        <>
                                            {

                                                (isEditing) ?
                                                    <div className='flex py-5 px-4' style={{ background: 'black', width: '100%', height: '100%' }}>
                                                        <div style={{ position: 'relative', width: '100%', height: '100%' }}>
                                                            <textarea className='vscDark vscDarkPre w-full' style={{ width: '100%', height: '98%' }} type="text" value={businessLogic} onChange={handleInputChange} />
                                                            <div style={{ position: 'absolute', top: '13px', right: '5px' }}>
                                                                <IconButton onClick={() => handleSaveClick(selectedLogicID)}>
                                                                    <Save sx={{ color: '#FFF' }} />
                                                                </IconButton>
                                                            </div>
                                                        </div>
                                                    </div>


                                                    :
                                                    <div className='flex py-5 px-4' style={{ background: 'black', width: '100%', height: '100%' }}>
                                                        <div style={{ position: 'relative', width: '100%' }}>
                                                            <LogicBlock businessLogic={businessLogic} />
                                                            <div style={{ position: 'absolute', top: '13px', right: '5px' }}>
                                                                <IconButton onClick={handleEditClick}>
                                                                    <Edit sx={{ color: '#FFF' }} />
                                                                </IconButton>
                                                            </div>
                                                        </div>
                                                    </div>

                                            }</>
                                }

                            </div>
                        </CustomTabPanel>

                        <CustomTabPanel value={value} index={1}>
                            <div className='flex p-5' style={{ background: 'black', width: '100%', height: '100%' }}>
                                
                                    {
                                        (diagramLoader) ? <>
                                            <div className='flex h-full w-full justify-center items-center'  ><CircularProgress /></div>
                                        </> :
                                        <div style={{ position: 'relative', width: '100%' }}>
                                            <div className='vscDark vscDarkPre' style={{ height: '93%' ,borderRadius: '15px'}}   >

                                                {
                                                    (flowchartCode === '') ?
                                                        <></> :
                                                        <div className=''>
                                                            <p className='text-lg font-black'>
                                                                FlowChart
                                                            </p>
                                                            <MermaidDiagram mermaidCode={flowchartCode} />
                                                        </div>
                                                }
                                                <Divider classes={{root:'customDivider'}} sx={{ bgcolor:'42a5f5'}} ></Divider>
                                                {
                                                    (classDiagramCode === '') ?
                                                        <></> :
                                                        <div className='mt-2'>
                                                            <p className='text-lg font-black'>
                                                                Class Diagram
                                                            </p>
                                                            <MermaidDiagram mermaidCode={classDiagramCode} />
                                                        </div>


                                                }


                                            </div>
                                            <div className='flex flex-col h-full bg-black w-5' style={{ position: 'absolute', top: '25px', right: '30px' }}>
                                        <Fab size='small' sx={{backgroundColor:'#42a5f5',":hover":{backgroundColor:'#64b5f6'}}} variant='outlined' onClick={() => handleDownload('mmd')}>
                                            <Download sx={{color:'#FFF'}}/>
                                        </Fab>
                                        <Fab size='small' sx={{backgroundColor:'#42a5f5',marginTop:'10px',":hover":{backgroundColor:'#64b5f6'}}} onClick={() => generateMermaidDiagramsNew(selectedLogicID)}>
                                            <ReplayOutlined sx={{color:'#FFF'}}/>
                                        </Fab>
                                    </div>

                                </div>
                                    }
                                    
                            </div>

                        </CustomTabPanel>
                        <CustomTabPanel value={value} index={2}>
                            <div className='flex py-7 px-4' style={{ background: 'black', width: '100%', height: '100%' }}>
                                
                                    {
                                        (javaLoader)?
                                        <>
                                            <div className='flex h-full w-full justify-center items-center'  ><CircularProgress /></div>
                                        </>
                                        :
                                        <div style={{ position: 'relative', width: '100%' }}>
                                        <AceEditor style={{ width: '100%', height: '95%' ,borderRadius:'15px' }}
                                        mode="python"
                                        theme="clouds_midnight"
                                        onChange={onChange}
                                        fontSize={14}
                                        showPrintMargin={true}
                                        showGutter={true}
                                        highlightActiveLine={true}
                                        value={javaCode}
                                        setOptions={{
                                            enableBasicAutocompletion: true,
                                            enableLiveAutocompletion: true,
                                            enableSnippets: true,
                                            showLineNumbers: true,
                                            tabSize: 2,
                                          }} />
                                        <div className='flex flex-col' style={{ position: 'absolute', top: '15px', right: '10px' }}>
                                        <Fab size='small' sx={{backgroundColor:'#42a5f5',":hover":{backgroundColor:'#64b5f6'}}} variant='outlined' onClick={() => handleDownload('java')}>
                                            <Download sx={{ color: '#FFF' }} />
                                        </Fab>
                                        <Fab size='small' sx={{backgroundColor:'#42a5f5',marginTop:'10px',":hover":{backgroundColor:'#64b5f6'}}} onClick={() => generateJavaCodeNew(selectedLogicID)}>
                                            <ReplayOutlined sx={{ color: '#FFF' }} />
                                        </Fab>
                                    </div>
                                    </div>
                                   
                                    }
                                    
                                    
                                

                            </div>


                        </CustomTabPanel>
                    </div>
                </div>
            </Split>
        </div >
    )
}
