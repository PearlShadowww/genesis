import { useState, useEffect } from 'react';
import {
  ChakraProvider,
  Box,
  VStack,
  HStack,
  Text,
  Button,
  Textarea,
  Card,
  CardBody,
  CardHeader,
  Heading,
  Badge,
  useToast,
  Flex,
  IconButton,
  Tooltip,
  Alert,
  AlertIcon,
  List,
  ListItem,
  ListIcon,
  Container,
  Input,
  InputGroup,
  InputRightElement,
  Divider,
  useColorModeValue,
} from '@chakra-ui/react';
import {
  Play,
  FolderOpen,
  FileText,
  Terminal,
  History,
  RefreshCw,
  CheckCircle,
  Code as CodeIcon,
  Copy,
  Download,
  Send,
  Sparkles,
  Zap,
  Globe,
  Settings,
} from 'lucide-react';

// Simplified interfaces
interface GeneratedFile {
  name: string;
  content: string;
  language: string;
  size?: number;
  lastModified?: Date;
}

interface ProjectHistory {
  id: string;
  prompt: string;
  timestamp: Date;
  status: 'success' | 'error' | 'pending';
  files: GeneratedFile[];
  project_path?: string;
}

function App() {
  // Simplified state management
  const [prompt, setPrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedFiles, setGeneratedFiles] = useState<GeneratedFile[]>([]);
  const [terminalOutput, setTerminalOutput] = useState<string[]>([]);
  const [projectHistory, setProjectHistory] = useState<ProjectHistory[]>([]);
  const [selectedFile, setSelectedFile] = useState<string | null>(null);
  const [backendStatus, setBackendStatus] = useState<'connected' | 'disconnected'>('disconnected');
  
  const toast = useToast();

  // Color mode values for better visibility
  const bgColor = useColorModeValue('white', 'gray.900');
  const textColor = useColorModeValue('gray.800', 'white');
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  const inputBg = useColorModeValue('white', 'gray.800');
  const cardBg = useColorModeValue('white', 'gray.800');

  // Check backend health on component mount
  useEffect(() => {
    checkBackendHealth();
  }, []);

  const checkBackendHealth = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8080/health', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      if (response.ok) {
        setBackendStatus('connected');
        addTerminalOutput('✅ Connected to Genesis backend');
      } else {
        setBackendStatus('disconnected');
        addTerminalOutput('❌ Backend health check failed');
      }
    } catch (error) {
      setBackendStatus('disconnected');
      addTerminalOutput('❌ Failed to connect to Genesis backend');
    }
  };

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      toast({
        title: 'Error',
        description: 'Please enter a project description',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    if (backendStatus === 'disconnected') {
      toast({
        title: 'Backend Disconnected',
        description: 'Please start the Genesis backend server first',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
      return;
    }

    setIsGenerating(true);
    setTerminalOutput([]);
    setGeneratedFiles([]);

    try {
      addTerminalOutput('🚀 Starting project generation...');
      addTerminalOutput(`📝 Prompt: ${prompt}`);
      
      // Call backend API
      const response = await fetch('http://127.0.0.1:8080/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt: prompt,
          backend: 'ollama'
        }),
      });

      if (!response.ok) {
        throw new Error(`Backend error: ${response.status}`);
      }

      const result = await response.json();
      addTerminalOutput('✅ Project generation request sent successfully');
      addTerminalOutput(`📋 Project ID: ${result.data}`);

      // Poll for project status
      await pollProjectStatus(result.data);

    } catch (error) {
      console.error('Generation error:', error);
      addTerminalOutput(`❌ Error: ${error instanceof Error ? error.message : 'Unknown error'}`);
      
      const failedProject: ProjectHistory = {
        id: Date.now().toString(),
        prompt,
        timestamp: new Date(),
        status: 'error',
        files: [],
      };
      
      setProjectHistory(prev => [failedProject, ...prev]);
      
      toast({
        title: 'Generation Failed',
        description: 'Failed to generate project. Check the terminal output for details.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsGenerating(false);
    }
  };

  const pollProjectStatus = async (projectId: string) => {
    const maxAttempts = 30; // 30 seconds max
    let attempts = 0;

    while (attempts < maxAttempts) {
      try {
        const response = await fetch(`http://127.0.0.1:8080/projects/${projectId}`);
        
        if (response.ok) {
          const result = await response.json();
          const project = result.data;

          addTerminalOutput(`📊 Status: ${project.status}`);

          if (project.status === 'completed') {
            addTerminalOutput('✅ Project generation completed!');
            
            // Convert files to our format
            const files: GeneratedFile[] = project.files.map((file: any) => ({
              name: file.name,
              content: file.content,
              language: file.language,
              size: file.size,
              lastModified: file.last_modified ? new Date(file.last_modified) : new Date(),
            }));

            setGeneratedFiles(files);
            
            // Add to history
            const newProject: ProjectHistory = {
              id: projectId,
              prompt,
              timestamp: new Date(project.created_at),
              status: 'success',
              files: files,
              project_path: project.project_path,
            };
            
            setProjectHistory(prev => [newProject, ...prev]);
            
            toast({
              title: 'Success',
              description: `Project generated successfully! Created ${files.length} files.`,
              status: 'success',
              duration: 5000,
              isClosable: true,
            });
            return;

          } else if (project.status === 'failed') {
            addTerminalOutput(`❌ Project generation failed: ${project.output}`);
            
            const failedProject: ProjectHistory = {
              id: projectId,
              prompt,
              timestamp: new Date(project.created_at),
              status: 'error',
              files: [],
            };
            
            setProjectHistory(prev => [failedProject, ...prev]);
            return;

          } else {
            // Still generating, wait and try again
            await new Promise(resolve => setTimeout(resolve, 1000));
            attempts++;
          }
        } else {
          throw new Error(`Failed to get project status: ${response.status}`);
        }
      } catch (error) {
        addTerminalOutput(`❌ Error polling project status: ${error}`);
        attempts++;
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
    }

    addTerminalOutput('⏰ Project generation timed out');
  };

  const addTerminalOutput = (message: string) => {
    setTerminalOutput(prev => [...prev, `[${new Date().toLocaleTimeString()}] ${message}`]);
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    toast({
      title: 'Copied',
      description: 'Code copied to clipboard',
      status: 'success',
      duration: 2000,
      isClosable: true,
    });
  };

  const downloadFile = (file: GeneratedFile) => {
    const blob = new Blob([file.content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = file.name;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      handleGenerate();
    }
  };

  return (
    <ChakraProvider>
      <Box minH="100vh" bg={bgColor} color={textColor}>
        {/* Header */}
        <Box 
          bg={cardBg} 
          borderBottom="1px" 
          borderColor={borderColor} 
          p={4}
          boxShadow="sm"
        >
          <Container maxW="7xl">
            <HStack justify="space-between">
              <HStack spacing={3}>
                <Box p={2} bg="blue.500" borderRadius="lg">
                  <Sparkles size={24} color="white" />
                </Box>
                <VStack align="start" spacing={0}>
                  <Heading size="lg" color="blue.500" fontWeight="bold">Genesis</Heading>
                  <Text fontSize="sm" color="gray.500">AI-Powered Code Generator</Text>
                </VStack>
              </HStack>
              <HStack spacing={4}>
                <Badge 
                  colorScheme={backendStatus === 'connected' ? 'green' : 'red'}
                  variant="subtle"
                  px={3}
                  py={1}
                  borderRadius="full"
                >
                  {backendStatus === 'connected' ? 'Connected' : 'Disconnected'}
                </Badge>
                <Tooltip label="Refresh connection">
                  <IconButton
                    aria-label="Refresh connection"
                    icon={<RefreshCw size={18} />}
                    variant="ghost"
                    colorScheme="blue"
                    onClick={checkBackendHealth}
                    size="sm"
                  />
                </Tooltip>
              </HStack>
            </HStack>
          </Container>
        </Box>

        <Container maxW="7xl" py={8}>
          <VStack spacing={8} align="stretch">
            {/* Connection Status Alert */}
            {backendStatus === 'disconnected' && (
              <Alert status="error" borderRadius="lg" bg="red.50" borderColor="red.200">
                <AlertIcon />
                <Box>
                  <Text fontWeight="bold" color="red.800">Genesis backend is not running</Text>
                  <Text fontSize="sm" color="red.600">Please start the backend server: cd backend && cargo run</Text>
                </Box>
              </Alert>
            )}

            {/* Main Input Section */}
            <Card bg={cardBg} borderColor={borderColor} boxShadow="lg">
              <CardBody p={8}>
                <VStack spacing={6}>
                  <VStack spacing={2} textAlign="center">
                    <Heading size="lg" color="gray.700">
                      Generate Code with AI
                    </Heading>
                    <Text color="gray.500" fontSize="lg">
                      Describe what you want to build and let AI create it for you
                    </Text>
                  </VStack>

                  <VStack spacing={4} w="full">
                    <Textarea
                      value={prompt}
                      onChange={(e) => setPrompt(e.target.value)}
                      onKeyPress={handleKeyPress}
                      placeholder="Describe the software project you want to generate... (e.g., 'Create a React todo app with add, delete, and mark complete functionality')"
                      size="lg"
                      bg={inputBg}
                      borderColor={borderColor}
                      _focus={{ 
                        borderColor: 'blue.400',
                        boxShadow: '0 0 0 1px var(--chakra-colors-blue-400)',
                        bg: inputBg
                      }}
                      _placeholder={{ color: 'gray.400' }}
                      rows={4}
                      fontSize="md"
                      resize="none"
                    />
                    
                    <Button
                      leftIcon={<Zap size={20} />}
                      bg="blue.500"
                      _hover={{ bg: 'blue.600' }}
                      _active={{ bg: 'blue.700' }}
                      color="white"
                      size="lg"
                      onClick={handleGenerate}
                      isLoading={isGenerating}
                      loadingText="Generating..."
                      w="full"
                      isDisabled={backendStatus === 'disconnected'}
                      borderRadius="lg"
                      py={6}
                      fontSize="md"
                      fontWeight="semibold"
                    >
                      Generate Project
                    </Button>
                    
                    <Text fontSize="sm" color="gray.400">
                      Press Ctrl+Enter to generate
                    </Text>
                  </VStack>
                </VStack>
              </CardBody>
            </Card>

            {/* Generated Files */}
            {generatedFiles.length > 0 && (
              <Card bg={cardBg} borderColor={borderColor} boxShadow="lg">
                <CardHeader pb={4}>
                  <HStack>
                    <FolderOpen size={20} color="#3182ce" />
                    <Heading size="md" color="gray.700">Generated Files</Heading>
                    <Badge colorScheme="green" variant="subtle">{generatedFiles.length} files</Badge>
                  </HStack>
                </CardHeader>
                <CardBody pt={0}>
                  <VStack spacing={4} align="stretch">
                    {generatedFiles.map((file, index) => (
                      <Box
                        key={index}
                        p={4}
                        bg={inputBg}
                        borderRadius="lg"
                        border="1px"
                        borderColor={borderColor}
                        cursor="pointer"
                        _hover={{ borderColor: 'blue.400', bg: 'blue.50' }}
                        onClick={() => setSelectedFile(file.name)}
                        transition="all 0.2s"
                      >
                        <HStack justify="space-between">
                          <HStack>
                            <FileText size={16} color="#3182ce" />
                            <Text fontWeight="medium" color="gray.700">{file.name}</Text>
                            <Badge size="sm" colorScheme="blue" variant="subtle">{file.language}</Badge>
                            {file.size && (
                              <Text fontSize="sm" color="gray.500">({Math.round(file.size / 1024)}KB)</Text>
                            )}
                          </HStack>
                          <HStack spacing={2}>
                            <Tooltip label="Copy code">
                              <IconButton
                                aria-label="Copy code"
                                size="sm"
                                icon={<Copy size={14} />}
                                onClick={(e) => {
                                  e.stopPropagation();
                                  copyToClipboard(file.content);
                                }}
                                variant="ghost"
                                colorScheme="blue"
                              />
                            </Tooltip>
                            <Tooltip label="Download file">
                              <IconButton
                                aria-label="Download file"
                                size="sm"
                                icon={<Download size={14} />}
                                onClick={(e) => {
                                  e.stopPropagation();
                                  downloadFile(file);
                                }}
                                variant="ghost"
                                colorScheme="green"
                              />
                            </Tooltip>
                          </HStack>
                        </HStack>
                      </Box>
                    ))}
                  </VStack>
                </CardBody>
              </Card>
            )}

            {/* Terminal Output */}
            <Card bg={cardBg} borderColor={borderColor} boxShadow="lg">
              <CardHeader pb={4}>
                <HStack>
                  <Terminal size={20} color="#3182ce" />
                  <Heading size="md" color="gray.700">Generation Log</Heading>
                </HStack>
              </CardHeader>
              <CardBody pt={0}>
                <Box
                  bg="gray.50"
                  p={4}
                  borderRadius="lg"
                  fontFamily="mono"
                  fontSize="sm"
                  maxH="300px"
                  overflowY="auto"
                  border="1px"
                  borderColor={borderColor}
                >
                  {terminalOutput.length > 0 ? (
                    terminalOutput.map((line, index) => (
                      <Text key={index} color="gray.600" mb={1}>{line}</Text>
                    ))
                  ) : (
                    <Text color="gray.400">No output yet...</Text>
                  )}
                </Box>
              </CardBody>
            </Card>
          </VStack>
        </Container>

        {/* Sidebar - Fixed Position */}
        <Box
          position="fixed"
          right={4}
          top="100px"
          w="350px"
          bg={cardBg}
          border="1px"
          borderColor={borderColor}
          borderRadius="lg"
          boxShadow="xl"
          p={4}
          maxH="calc(100vh - 120px)"
          overflowY="auto"
        >
          <VStack spacing={6} align="stretch">
            {/* Project History */}
            <Box>
              <HStack mb={4}>
                <History size={18} color="#3182ce" />
                <Heading size="sm" color="gray.700">Project History</Heading>
              </HStack>
              <VStack spacing={3} align="stretch" maxH="200px" overflowY="auto">
                {projectHistory.map((project) => (
                  <Box
                    key={project.id}
                    p={3}
                    bg={inputBg}
                    borderRadius="md"
                    cursor="pointer"
                    _hover={{ bg: 'blue.50' }}
                    border="1px"
                    borderColor={borderColor}
                  >
                    <VStack align="start" spacing={2}>
                      <HStack justify="space-between" w="full">
                        <Text fontSize="sm" fontWeight="medium" noOfLines={2} color="gray.700">
                          {project.prompt}
                        </Text>
                        <Badge
                          size="sm"
                          colorScheme={project.status === 'success' ? 'green' : 'red'}
                          variant="subtle"
                        >
                          {project.status}
                        </Badge>
                      </HStack>
                      <Text fontSize="xs" color="gray.500">
                        {project.timestamp.toLocaleString()}
                      </Text>
                      {project.files.length > 0 && (
                        <Text fontSize="xs" color="gray.500">
                          {project.files.length} files generated
                        </Text>
                      )}
                      {project.project_path && (
                        <Text fontSize="xs" color="blue.500" fontWeight="medium">
                          📁 {project.project_path.split('/').pop() || project.project_path}
                        </Text>
                      )}
                    </VStack>
                  </Box>
                ))}
                {projectHistory.length === 0 && (
                  <Text color="gray.400" fontSize="sm" textAlign="center">
                    No projects generated yet
                  </Text>
                )}
              </VStack>
            </Box>

            <Divider />

            {/* File Preview */}
            {selectedFile && (
              <Box>
                <HStack mb={4}>
                  <FileText size={18} color="#3182ce" />
                  <Heading size="sm" color="gray.700">File Preview</Heading>
                </HStack>
                <Box
                  bg="gray.50"
                  p={4}
                  borderRadius="md"
                  fontFamily="mono"
                  fontSize="xs"
                  maxH="300px"
                  overflowY="auto"
                  border="1px"
                  borderColor={borderColor}
                >
                  <Text color="gray.700">
                    {generatedFiles.find(f => f.name === selectedFile)?.content}
                  </Text>
                </Box>
              </Box>
            )}
          </VStack>
        </Box>
      </Box>
    </ChakraProvider>
  );
}

export default App;
  