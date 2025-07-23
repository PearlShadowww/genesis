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
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  Select,
  Input,
  Switch,
  FormControl,
  FormLabel,
  Radio,
  RadioGroup,
  Stack,
  Tag,
  TagLabel,
  Wrap,
  WrapItem,
  Progress,
  Alert,
  AlertIcon,
  List,
  ListItem,
  ListIcon,
  Grid,
  GridItem,
} from '@chakra-ui/react';
import {
  Play,
  FolderOpen,
  FileText,
  Terminal,
  History,
  Settings,
  Download,
  Copy,
  Code as CodeIcon,
  Plus,
  Trash2,
  RefreshCw,
  CheckCircle,
  Rocket,
  Package,
  Users,
  BarChart3,
  BookOpen,
  ShoppingCart,
  Layers,
} from 'lucide-react';

// Enhanced interfaces for comprehensive features
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
  projectType?: string;
  framework?: string;
  complexity?: string;
}

interface ProjectTemplate {
  id: string;
  name: string;
  description: string;
  category: string;
  icon: any;
  tags: string[];
  complexity: 'beginner' | 'intermediate' | 'advanced';
  estimatedTime: string;
  features: string[];
}

interface GenerationSettings {
  framework: string;
  language: string;
  complexity: string;
  includeTests: boolean;
  includeDocs: boolean;
  includeCI: boolean;
  includeDocker: boolean;
  includeAPI: boolean;
  includeDatabase: boolean;
  includeAuth: boolean;
  includeUI: boolean;
  customFeatures: string[];
}

interface ProjectStructure {
  type: 'monorepo' | 'microservices' | 'single-app' | 'spa' | 'ssr';
  frontend: string[];
  backend: string[];
  database: string[];
  infrastructure: string[];
  testing: string[];
  documentation: string[];
}

function App() {
  // State management for comprehensive features
  const [prompt, setPrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedFiles, setGeneratedFiles] = useState<GeneratedFile[]>([]);
  const [terminalOutput, setTerminalOutput] = useState<string[]>([]);
  const [projectHistory, setProjectHistory] = useState<ProjectHistory[]>([]);
  const [selectedFile, setSelectedFile] = useState<string | null>(null);
  const [backendStatus, setBackendStatus] = useState<'connected' | 'disconnected'>('disconnected');
  const [activeTab, setActiveTab] = useState(0);
  const [generationSettings, setGenerationSettings] = useState<GenerationSettings>({
    framework: 'react',
    language: 'typescript',
    complexity: 'intermediate',
    includeTests: true,
    includeDocs: true,
    includeCI: false,
    includeDocker: false,
    includeAPI: true,
    includeDatabase: false,
    includeAuth: false,
    includeUI: true,
    customFeatures: [],
  });
  const [projectStructure, setProjectStructure] = useState<ProjectStructure>({
    type: 'single-app',
    frontend: ['components', 'pages', 'hooks', 'utils'],
    backend: ['api', 'middleware', 'models'],
    database: ['migrations', 'seeds'],
    infrastructure: ['docker', 'kubernetes'],
    testing: ['unit', 'integration', 'e2e'],
    documentation: ['readme', 'api-docs', 'deployment'],
  });
  const [, setSelectedTemplate] = useState<ProjectTemplate | null>(null);
  // const [showAdvancedSettings, setShowAdvancedSettings] = useState(false);
  const [generationProgress, setGenerationProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState('');
  
  const toast = useToast();
  // Modal controls for future use
  const onHistoryOpen = () => toast({ title: 'History', description: 'History panel coming soon', status: 'info' });
  const onSettingsOpen = () => toast({ title: 'Settings', description: 'Settings panel coming soon', status: 'info' });

  // Project templates for quick start
  const projectTemplates: ProjectTemplate[] = [
    {
      id: 'ecommerce',
      name: 'E-commerce Platform',
      description: 'Full-stack e-commerce with payment integration',
      category: 'Business',
      icon: ShoppingCart,
      tags: ['react', 'nodejs', 'mongodb', 'stripe'],
      complexity: 'advanced',
      estimatedTime: '2-3 hours',
      features: ['User authentication', 'Product catalog', 'Shopping cart', 'Payment processing', 'Order management', 'Admin dashboard'],
    },
    {
      id: 'social-media',
      name: 'Social Media App',
      description: 'Social networking platform with real-time features',
      category: 'Social',
      icon: Users,
      tags: ['react', 'socket.io', 'postgresql', 'redis'],
      complexity: 'advanced',
      estimatedTime: '3-4 hours',
      features: ['User profiles', 'Posts & comments', 'Real-time messaging', 'News feed', 'Friend system', 'Notifications'],
    },
    {
      id: 'task-manager',
      name: 'Task Management App',
      description: 'Project management with team collaboration',
      category: 'Productivity',
      icon: CheckCircle,
      tags: ['react', 'express', 'sqlite', 'jwt'],
      complexity: 'intermediate',
      estimatedTime: '1-2 hours',
      features: ['Task creation', 'Team collaboration', 'Progress tracking', 'File sharing', 'Calendar integration', 'Reports'],
    },
    {
      id: 'blog-platform',
      name: 'Blog Platform',
      description: 'Content management system for bloggers',
      category: 'Content',
      icon: BookOpen,
      tags: ['nextjs', 'prisma', 'postgresql', 'markdown'],
      complexity: 'intermediate',
      estimatedTime: '1-2 hours',
      features: ['Article editor', 'SEO optimization', 'Comment system', 'User management', 'Analytics', 'RSS feeds'],
    },
    {
      id: 'dashboard',
      name: 'Analytics Dashboard',
      description: 'Data visualization and analytics platform',
      category: 'Analytics',
      icon: BarChart3,
      tags: ['react', 'd3', 'express', 'mongodb'],
      complexity: 'advanced',
      estimatedTime: '2-3 hours',
      features: ['Data visualization', 'Real-time charts', 'Export functionality', 'User permissions', 'Custom reports', 'API integration'],
    },
    {
      id: 'mobile-app',
      name: 'Mobile App',
      description: 'Cross-platform mobile application',
      category: 'Mobile',
      icon: Users, // Changed from Smartphone to Users as per new_code
      tags: ['react-native', 'expo', 'firebase', 'redux'],
      complexity: 'advanced',
      estimatedTime: '2-3 hours',
      features: ['Cross-platform', 'Push notifications', 'Offline support', 'Camera integration', 'GPS tracking', 'Social sharing'],
    },
  ];

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
    setGenerationProgress(0);

    try {
      addTerminalOutput('🚀 Starting project generation...');
      addTerminalOutput(`📝 Prompt: ${prompt}`);
      addTerminalOutput('⚙️ Applying generation settings...');
      
      // Simulate generation steps
      const steps = [
        'Analyzing requirements...',
        'Designing architecture...',
        'Generating frontend components...',
        'Creating backend API...',
        'Setting up database...',
        'Adding authentication...',
        'Implementing features...',
        'Writing tests...',
        'Creating documentation...',
        'Finalizing project...'
      ];

      for (let i = 0; i < steps.length; i++) {
        setCurrentStep(steps[i]);
        setGenerationProgress((i + 1) * 10);
        addTerminalOutput(`🔄 ${steps[i]}`);
        await new Promise(resolve => setTimeout(resolve, 1000));
      }

      // Simulate generated files
      const mockFiles: GeneratedFile[] = [
        {
          name: 'package.json',
          content: JSON.stringify({ name: 'generated-project', version: '1.0.0' }, null, 2),
          language: 'json',
          size: 1024,
          lastModified: new Date(),
        },
        {
          name: 'src/App.tsx',
          content: 'import React from "react";\n\nfunction App() {\n  return <div>Generated App</div>;\n}\n\nexport default App;',
          language: 'typescript',
          size: 2048,
          lastModified: new Date(),
        },
        {
          name: 'README.md',
          content: '# Generated Project\n\nThis project was generated by Genesis AI.',
          language: 'markdown',
          size: 512,
          lastModified: new Date(),
        },
      ];

      setGeneratedFiles(mockFiles);
      addTerminalOutput('✅ Project generation completed!');
      
      // Add to history
      const newProject: ProjectHistory = {
        id: Date.now().toString(),
        prompt,
        timestamp: new Date(),
        status: 'success',
        files: mockFiles,
        projectType: generationSettings.framework,
        framework: generationSettings.language,
        complexity: generationSettings.complexity,
      };
      
      setProjectHistory(prev => [newProject, ...prev]);
      
      toast({
        title: 'Success',
        description: `Project generated successfully! Created ${mockFiles.length} files.`,
        status: 'success',
        duration: 5000,
        isClosable: true,
      });

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
      setGenerationProgress(0);
      setCurrentStep('');
    }
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

  const downloadProject = () => {
    // Create a zip file with all generated files
    toast({
      title: 'Download Started',
      description: 'Project files are being prepared for download...',
      status: 'info',
      duration: 3000,
      isClosable: true,
    });
  };

  const applyTemplate = (template: ProjectTemplate) => {
    setSelectedTemplate(template);
    setPrompt(`Create a ${template.name.toLowerCase()} with the following features: ${template.features.join(', ')}`);
    
    // Update generation settings based on template
    const templateSettings = { ...generationSettings };
    if (template.tags.includes('react')) templateSettings.framework = 'react';
    if (template.tags.includes('typescript')) templateSettings.language = 'typescript';
    if (template.complexity === 'advanced') templateSettings.complexity = 'advanced';
    
    setGenerationSettings(templateSettings);
    
    toast({
      title: 'Template Applied',
      description: `${template.name} template has been applied`,
      status: 'success',
      duration: 3000,
      isClosable: true,
    });
  };

  return (
    <ChakraProvider>
      <Box minH="100vh" bg="black" color="white">
        {/* Header */}
        <Box bg="gray.900" borderBottom="1px" borderColor="gray.800" p={4}>
          <HStack justify="space-between">
            <HStack>
              <CodeIcon size={32} color="#ff8c00" />
              <VStack align="start" spacing={0}>
                <Heading size="lg" bgGradient="linear(to-r, orange.400, yellow.400)" bgClip="text">Genesis</Heading>
                <Text fontSize="sm" color="gray.300">AI-Powered Software Generator</Text>
              </VStack>
            </HStack>
            <HStack spacing={4}>
              <Badge 
                colorScheme={backendStatus === 'connected' ? 'green' : 'red'}
                variant="subtle"
              >
                {backendStatus === 'connected' ? 'Connected' : 'Disconnected'}
              </Badge>
              <Tooltip label="Project History">
                <IconButton
                  aria-label="Project History"
                  icon={<History size={20} />}
                  variant="ghost"
                  colorScheme="orange"
                  onClick={onHistoryOpen}
                />
              </Tooltip>
              <Tooltip label="Advanced Settings">
                <IconButton
                  aria-label="Advanced Settings"
                  icon={<Settings size={20} />}
                  variant="ghost"
                  colorScheme="orange"
                  onClick={onSettingsOpen}
                />
              </Tooltip>
              <Tooltip label="Refresh connection">
                <IconButton
                  aria-label="Refresh connection"
                  icon={<RefreshCw size={20} />}
                  variant="ghost"
                  colorScheme="orange"
                  onClick={checkBackendHealth}
                />
              </Tooltip>
            </HStack>
          </HStack>
        </Box>

        <Flex h="calc(100vh - 80px)">
          {/* Main Content */}
          <VStack flex={1} p={6} spacing={6} align="stretch">
            {/* Connection Status Alert */}
            {backendStatus === 'disconnected' && (
              <Alert status="error" borderRadius="md" bg="red.900" borderColor="red.700">
                <AlertIcon />
                <Box>
                  <Text fontWeight="bold">Genesis backend is not running</Text>
                  <Text fontSize="sm">Please start the backend server: cd backend && cargo run</Text>
                </Box>
              </Alert>
            )}

            {/* Main Tabs */}
            <Tabs index={activeTab} onChange={setActiveTab} variant="enclosed" colorScheme="orange">
              <TabList>
                <Tab>🚀 Quick Start</Tab>
                <Tab>⚙️ Advanced</Tab>
                <Tab>📋 Templates</Tab>
                <Tab>🏗️ Structure</Tab>
                <Tab>📊 Results</Tab>
              </TabList>

              <TabPanels>
                {/* Quick Start Tab */}
                <TabPanel>
                  <VStack spacing={6} align="stretch">
                    <Card bg="gray.900" borderColor="gray.800">
                      <CardHeader>
                        <HStack>
                          <Rocket size={20} color="#ff8c00" />
                          <Heading size="md" bgGradient="linear(to-r, orange.400, yellow.400)" bgClip="text">Quick Project Generation</Heading>
                        </HStack>
                      </CardHeader>
                      <CardBody>
                        <VStack spacing={4}>
                          <Textarea
                            value={prompt}
                            onChange={(e) => setPrompt(e.target.value)}
                            placeholder="Describe the software project you want to generate... (e.g., 'Create a React todo app with add, delete, and mark complete functionality')"
                            size="lg"
                            bg="gray.800"
                            borderColor="gray.700"
                            _focus={{ borderColor: 'orange.400' }}
                            rows={4}
                          />
                          <HStack spacing={4} w="full">
                            <Select
                              value={generationSettings.framework}
                              onChange={(e) => setGenerationSettings(prev => ({ ...prev, framework: e.target.value }))}
                              bg="gray.800"
                              borderColor="gray.700"
                            >
                              <option value="react">React</option>
                              <option value="vue">Vue.js</option>
                              <option value="angular">Angular</option>
                              <option value="nextjs">Next.js</option>
                              <option value="nuxt">Nuxt.js</option>
                              <option value="svelte">Svelte</option>
                              <option value="flutter">Flutter</option>
                              <option value="react-native">React Native</option>
                            </Select>
                            <Select
                              value={generationSettings.language}
                              onChange={(e) => setGenerationSettings(prev => ({ ...prev, language: e.target.value }))}
                              bg="gray.800"
                              borderColor="gray.700"
                            >
                              <option value="typescript">TypeScript</option>
                              <option value="javascript">JavaScript</option>
                              <option value="python">Python</option>
                              <option value="java">Java</option>
                              <option value="csharp">C#</option>
                              <option value="go">Go</option>
                              <option value="rust">Rust</option>
                            </Select>
                            <Select
                              value={generationSettings.complexity}
                              onChange={(e) => setGenerationSettings(prev => ({ ...prev, complexity: e.target.value }))}
                              bg="gray.800"
                              borderColor="gray.700"
                            >
                              <option value="beginner">Beginner</option>
                              <option value="intermediate">Intermediate</option>
                              <option value="advanced">Advanced</option>
                            </Select>
                          </HStack>
                          <Button
                            leftIcon={<Play size={20} />}
                            bgGradient="linear(to-r, orange.400, yellow.400)"
                            _hover={{ bgGradient: "linear(to-r, orange.500, yellow.500)" }}
                            color="black"
                            size="lg"
                            onClick={handleGenerate}
                            isLoading={isGenerating}
                            loadingText="Generating..."
                            w="full"
                            isDisabled={backendStatus === 'disconnected'}
                          >
                            Generate Project
                          </Button>
                        </VStack>
                      </CardBody>
                    </Card>

                    {/* Generation Progress */}
                    {isGenerating && (
                      <Card bg="gray.900" borderColor="gray.800">
                        <CardBody>
                          <VStack spacing={4}>
                            <Text fontWeight="medium">{currentStep}</Text>
                            <Progress 
                              value={generationProgress} 
                              bg="gray.800"
                              sx={{
                                '& > div': {
                                  background: 'linear-gradient(to right, #ff8c00, #ffd700)'
                                }
                              }}
                              size="lg" 
                              w="full" 
                            />
                            <Text fontSize="sm" color="gray.300">{generationProgress}% Complete</Text>
                          </VStack>
                        </CardBody>
                      </Card>
                    )}
                  </VStack>
                </TabPanel>

                {/* Advanced Tab */}
                <TabPanel>
                  <VStack spacing={6} align="stretch">
                    <Card bg="gray.900" borderColor="gray.800">
                      <CardHeader>
                        <HStack>
                          <Settings size={20} color="#ff8c00" />
                          <Heading size="md" bgGradient="linear(to-r, orange.400, yellow.400)" bgClip="text">Advanced Generation Settings</Heading>
                        </HStack>
                      </CardHeader>
                      <CardBody>
                        <Grid templateColumns="repeat(2, 1fr)" gap={6}>
                          <GridItem>
                            <VStack spacing={4} align="stretch">
                              <FormControl>
                                <FormLabel>Framework</FormLabel>
                                <Select
                                  value={generationSettings.framework}
                                  onChange={(e) => setGenerationSettings(prev => ({ ...prev, framework: e.target.value }))}
                                  bg="gray.800"
                                  borderColor="gray.700"
                                >
                                  <option value="react">React</option>
                                  <option value="vue">Vue.js</option>
                                  <option value="angular">Angular</option>
                                  <option value="nextjs">Next.js</option>
                                  <option value="nuxt">Nuxt.js</option>
                                  <option value="svelte">Svelte</option>
                                  <option value="flutter">Flutter</option>
                                  <option value="react-native">React Native</option>
                                </Select>
                              </FormControl>

                              <FormControl>
                                <FormLabel>Language</FormLabel>
                                <Select
                                  value={generationSettings.language}
                                  onChange={(e) => setGenerationSettings(prev => ({ ...prev, language: e.target.value }))}
                                  bg="gray.800"
                                  borderColor="gray.700"
                                >
                                  <option value="typescript">TypeScript</option>
                                  <option value="javascript">JavaScript</option>
                                  <option value="python">Python</option>
                                  <option value="java">Java</option>
                                  <option value="csharp">C#</option>
                                  <option value="go">Go</option>
                                  <option value="rust">Rust</option>
                                </Select>
                              </FormControl>

                              <FormControl>
                                <FormLabel>Complexity</FormLabel>
                                <Select
                                  value={generationSettings.complexity}
                                  onChange={(e) => setGenerationSettings(prev => ({ ...prev, complexity: e.target.value }))}
                                  bg="gray.800"
                                  borderColor="gray.700"
                                >
                                  <option value="beginner">Beginner</option>
                                  <option value="intermediate">Intermediate</option>
                                  <option value="advanced">Advanced</option>
                                </Select>
                              </FormControl>
                            </VStack>
                          </GridItem>

                          <GridItem>
                            <VStack spacing={4} align="stretch">
                              <FormControl display="flex" alignItems="center">
                                <FormLabel mb="0">Include Tests</FormLabel>
                                <Switch
                                  isChecked={generationSettings.includeTests}
                                  onChange={(e) => setGenerationSettings(prev => ({ ...prev, includeTests: e.target.checked }))}
                                  colorScheme="orange"
                                />
                              </FormControl>

                              <FormControl display="flex" alignItems="center">
                                <FormLabel mb="0">Include Documentation</FormLabel>
                                <Switch
                                  isChecked={generationSettings.includeDocs}
                                  onChange={(e) => setGenerationSettings(prev => ({ ...prev, includeDocs: e.target.checked }))}
                                  colorScheme="orange"
                                />
                              </FormControl>

                              <FormControl display="flex" alignItems="center">
                                <FormLabel mb="0">Include CI/CD</FormLabel>
                                <Switch
                                  isChecked={generationSettings.includeCI}
                                  onChange={(e) => setGenerationSettings(prev => ({ ...prev, includeCI: e.target.checked }))}
                                  colorScheme="orange"
                                />
                              </FormControl>

                              <FormControl display="flex" alignItems="center">
                                <FormLabel mb="0">Include Docker</FormLabel>
                                <Switch
                                  isChecked={generationSettings.includeDocker}
                                  onChange={(e) => setGenerationSettings(prev => ({ ...prev, includeDocker: e.target.checked }))}
                                  colorScheme="orange"
                                />
                              </FormControl>

                              <FormControl display="flex" alignItems="center">
                                <FormLabel mb="0">Include API</FormLabel>
                                <Switch
                                  isChecked={generationSettings.includeAPI}
                                  onChange={(e) => setGenerationSettings(prev => ({ ...prev, includeAPI: e.target.checked }))}
                                  colorScheme="orange"
                                />
                              </FormControl>

                              <FormControl display="flex" alignItems="center">
                                <FormLabel mb="0">Include Database</FormLabel>
                                <Switch
                                  isChecked={generationSettings.includeDatabase}
                                  onChange={(e) => setGenerationSettings(prev => ({ ...prev, includeDatabase: e.target.checked }))}
                                  colorScheme="orange"
                                />
                              </FormControl>

                              <FormControl display="flex" alignItems="center">
                                <FormLabel mb="0">Include Authentication</FormLabel>
                                <Switch
                                  isChecked={generationSettings.includeAuth}
                                  onChange={(e) => setGenerationSettings(prev => ({ ...prev, includeAuth: e.target.checked }))}
                                  colorScheme="orange"
                                />
                              </FormControl>

                              <FormControl display="flex" alignItems="center">
                                <FormLabel mb="0">Include UI Components</FormLabel>
                                <Switch
                                  isChecked={generationSettings.includeUI}
                                  onChange={(e) => setGenerationSettings(prev => ({ ...prev, includeUI: e.target.checked }))}
                                  colorScheme="orange"
                                />
                              </FormControl>
                            </VStack>
                          </GridItem>
                        </Grid>
                      </CardBody>
                    </Card>
                  </VStack>
                </TabPanel>

                {/* Templates Tab */}
                <TabPanel>
                  <VStack spacing={6} align="stretch">
                    <Card bg="gray.900" borderColor="gray.800">
                      <CardHeader>
                        <HStack>
                          <Package size={20} color="#ff8c00" />
                          <Heading size="md" bgGradient="linear(to-r, orange.400, yellow.400)" bgClip="text">Project Templates</Heading>
                        </HStack>
                      </CardHeader>
                      <CardBody>
                        <Grid templateColumns="repeat(auto-fit, minmax(300px, 1fr))" gap={6}>
                          {projectTemplates.map((template) => (
                            <Card key={template.id} bg="gray.800" borderColor="gray.700" cursor="pointer" _hover={{ borderColor: 'orange.400' }} onClick={() => applyTemplate(template)}>
                              <CardBody>
                                <VStack spacing={4} align="start">
                                  <HStack>
                                    <template.icon size={24} color="#ff8c00" />
                                    <VStack align="start" spacing={0}>
                                      <Heading size="md">{template.name}</Heading>
                                      <Text fontSize="sm" color="gray.300">{template.category}</Text>
                                    </VStack>
                                  </HStack>
                                  <Text fontSize="sm">{template.description}</Text>
                                  <Wrap>
                                    {template.tags.map((tag) => (
                                      <WrapItem key={tag}>
                                        <Tag size="sm" bgGradient="linear(to-r, orange.400, yellow.400)" color="black" variant="solid">
                                          <TagLabel>{tag}</TagLabel>
                                        </Tag>
                                      </WrapItem>
                                    ))}
                                  </Wrap>
                                  <HStack justify="space-between" w="full">
                                    <Badge 
                                      bgGradient={template.complexity === 'advanced' ? 'linear(to-r, red.400, red.600)' : template.complexity === 'intermediate' ? 'linear(to-r, orange.400, yellow.400)' : 'linear(to-r, green.400, green.600)'}
                                      color="black"
                                    >
                                      {template.complexity}
                                    </Badge>
                                    <Text fontSize="sm" color="gray.300">{template.estimatedTime}</Text>
                                  </HStack>
                                  <VStack align="start" spacing={1}>
                                    <Text fontSize="sm" fontWeight="medium">Features:</Text>
                                    <List spacing={1}>
                                      {template.features.slice(0, 3).map((feature, index) => (
                                        <ListItem key={index} fontSize="sm" color="gray.300">
                                          <ListIcon as={CheckCircle} color="#ff8c00" />
                                          {feature}
                                        </ListItem>
                                      ))}
                                      {template.features.length > 3 && (
                                        <ListItem fontSize="sm" color="gray.400">
                                          +{template.features.length - 3} more features
                                        </ListItem>
                                      )}
                                    </List>
                                  </VStack>
                                </VStack>
                              </CardBody>
                            </Card>
                          ))}
                        </Grid>
                      </CardBody>
                    </Card>
                  </VStack>
                </TabPanel>

                {/* Structure Tab */}
                <TabPanel>
                  <VStack spacing={6} align="stretch">
                    <Card bg="gray.900" borderColor="gray.800">
                      <CardHeader>
                        <HStack>
                          <Layers size={20} color="#ff8c00" />
                          <Heading size="md" bgGradient="linear(to-r, orange.400, yellow.400)" bgClip="text">Project Structure Builder</Heading>
                        </HStack>
                      </CardHeader>
                      <CardBody>
                        <VStack spacing={6} align="stretch">
                          <FormControl>
                            <FormLabel>Project Type</FormLabel>
                            <RadioGroup value={projectStructure.type} onChange={(value) => setProjectStructure(prev => ({ ...prev, type: value as any }))}>
                              <Stack direction="row">
                                <Radio value="single-app">Single App</Radio>
                                <Radio value="monorepo">Monorepo</Radio>
                                <Radio value="microservices">Microservices</Radio>
                                <Radio value="spa">SPA</Radio>
                                <Radio value="ssr">SSR</Radio>
                              </Stack>
                            </RadioGroup>
                          </FormControl>

                          <Grid templateColumns="repeat(2, 1fr)" gap={6}>
                            <VStack spacing={4} align="stretch">
                              <Heading size="sm">Frontend Structure</Heading>
                              <VStack spacing={2} align="stretch">
                                {projectStructure.frontend.map((item, index) => (
                                  <HStack key={index}>
                                    <Input
                                      value={item}
                                      onChange={(e) => {
                                        const newFrontend = [...projectStructure.frontend];
                                        newFrontend[index] = e.target.value;
                                        setProjectStructure(prev => ({ ...prev, frontend: newFrontend }));
                                      }}
                                      bg="gray.800"
                                      borderColor="gray.700"
                                      size="sm"
                                    />
                                    <IconButton
                                      aria-label="Remove item"
                                      icon={<Trash2 size={16} />}
                                      size="sm"
                                      variant="ghost"
                                      colorScheme="red"
                                      onClick={() => {
                                        const newFrontend = projectStructure.frontend.filter((_, i) => i !== index);
                                        setProjectStructure(prev => ({ ...prev, frontend: newFrontend }));
                                      }}
                                    />
                                  </HStack>
                                ))}
                                <Button
                                  leftIcon={<Plus size={16} />}
                                  size="sm"
                                  variant="outline"
                                  borderColor="orange.400"
                                  color="orange.400"
                                  _hover={{ bg: 'orange.400', color: 'black' }}
                                  onClick={() => setProjectStructure(prev => ({ ...prev, frontend: [...prev.frontend, 'new-folder'] }))}
                                >
                                  Add Frontend Folder
                                </Button>
                              </VStack>
                            </VStack>

                            <VStack spacing={4} align="stretch">
                              <Heading size="sm">Backend Structure</Heading>
                              <VStack spacing={2} align="stretch">
                                {projectStructure.backend.map((item, index) => (
                                  <HStack key={index}>
                                    <Input
                                      value={item}
                                      onChange={(e) => {
                                        const newBackend = [...projectStructure.backend];
                                        newBackend[index] = e.target.value;
                                        setProjectStructure(prev => ({ ...prev, backend: newBackend }));
                                      }}
                                      bg="gray.800"
                                      borderColor="gray.700"
                                      size="sm"
                                    />
                                    <IconButton
                                      aria-label="Remove item"
                                      icon={<Trash2 size={16} />}
                                      size="sm"
                                      variant="ghost"
                                      colorScheme="red"
                                      onClick={() => {
                                        const newBackend = projectStructure.backend.filter((_, i) => i !== index);
                                        setProjectStructure(prev => ({ ...prev, backend: newBackend }));
                                      }}
                                    />
                                  </HStack>
                                ))}
                                <Button
                                  leftIcon={<Plus size={16} />}
                                  size="sm"
                                  variant="outline"
                                  borderColor="orange.400"
                                  color="orange.400"
                                  _hover={{ bg: 'orange.400', color: 'black' }}
                                  onClick={() => setProjectStructure(prev => ({ ...prev, backend: [...prev.backend, 'new-folder'] }))}
                                >
                                  Add Backend Folder
                                </Button>
                              </VStack>
                            </VStack>
                          </Grid>
                        </VStack>
                      </CardBody>
                    </Card>
                  </VStack>
                </TabPanel>

                {/* Results Tab */}
                <TabPanel>
                  <VStack spacing={6} align="stretch">
                    {/* Generated Files */}
                    {generatedFiles.length > 0 && (
                      <Card bg="gray.900" borderColor="gray.800">
                        <CardHeader>
                          <HStack justify="space-between">
                            <HStack>
                              <FolderOpen size={20} color="#ff8c00" />
                              <Heading size="md" bgGradient="linear(to-r, orange.400, yellow.400)" bgClip="text">Generated Files</Heading>
                              <Badge bgGradient="linear(to-r, green.400, green.600)" color="black">{generatedFiles.length} files</Badge>
                            </HStack>
                            <HStack>
                              <Button
                                leftIcon={<Download size={16} />}
                                size="sm"
                                variant="outline"
                                borderColor="orange.400"
                                color="orange.400"
                                _hover={{ bg: 'orange.400', color: 'black' }}
                                onClick={downloadProject}
                              >
                                Download All
                              </Button>
                            </HStack>
                          </HStack>
                        </CardHeader>
                        <CardBody>
                          <VStack spacing={4} align="stretch">
                            {generatedFiles.map((file, index) => (
                              <Box
                                key={index}
                                p={4}
                                bg="gray.800"
                                borderRadius="md"
                                border="1px"
                                borderColor="gray.700"
                                cursor="pointer"
                                _hover={{ borderColor: 'orange.400' }}
                                onClick={() => setSelectedFile(file.name)}
                              >
                                <HStack justify="space-between">
                                  <HStack>
                                    <FileText size={16} color="#ff8c00" />
                                    <Text fontWeight="medium">{file.name}</Text>
                                    <Badge size="sm" bgGradient="linear(to-r, orange.400, yellow.400)" color="black">{file.language}</Badge>
                                    {file.size && (
                                      <Text fontSize="sm" color="gray.300">({Math.round(file.size / 1024)}KB)</Text>
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
                                        colorScheme="orange"
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
                    <Card bg="gray.900" borderColor="gray.800">
                      <CardHeader>
                        <HStack>
                          <Terminal size={20} color="#ff8c00" />
                          <Heading size="md" bgGradient="linear(to-r, orange.400, yellow.400)" bgClip="text">Generation Log</Heading>
                        </HStack>
                      </CardHeader>
                      <CardBody>
                        <Box
                          bg="black"
                          p={4}
                          borderRadius="md"
                          fontFamily="mono"
                          fontSize="sm"
                          maxH="300px"
                          overflowY="auto"
                        >
                          {terminalOutput.length > 0 ? (
                            terminalOutput.map((line, index) => (
                              <Text key={index} color="gray.300">{line}</Text>
                            ))
                          ) : (
                            <Text color="gray.500">No output yet...</Text>
                          )}
                        </Box>
                      </CardBody>
                    </Card>
                  </VStack>
                </TabPanel>
              </TabPanels>
            </Tabs>
          </VStack>

          {/* Sidebar */}
          <Box w="400px" bg="gray.900" borderLeft="1px" borderColor="gray.800" p={4}>
            <VStack spacing={6} align="stretch">
              {/* Project History */}
              <Box>
                <HStack mb={4}>
                  <History size={20} color="#ff8c00" />
                  <Heading size="md" bgGradient="linear(to-r, orange.400, yellow.400)" bgClip="text">Project History</Heading>
                </HStack>
                <VStack spacing={3} align="stretch" maxH="300px" overflowY="auto">
                  {projectHistory.map((project) => (
                    <Box
                      key={project.id}
                      p={3}
                      bg="gray.800"
                      borderRadius="md"
                      cursor="pointer"
                      _hover={{ bg: 'gray.700' }}
                    >
                      <VStack align="start" spacing={2}>
                        <HStack justify="space-between" w="full">
                          <Text fontSize="sm" fontWeight="medium" noOfLines={2}>
                            {project.prompt}
                          </Text>
                          <Badge
                            size="sm"
                            bgGradient={project.status === 'success' ? 'linear(to-r, green.400, green.600)' : 'linear(to-r, red.400, red.600)'}
                            color="black"
                          >
                            {project.status}
                          </Badge>
                        </HStack>
                        <Text fontSize="xs" color="gray.400">
                          {project.timestamp.toLocaleString()}
                        </Text>
                        {project.framework && (
                          <HStack spacing={2}>
                            <Badge size="sm" variant="outline" borderColor="orange.400" color="orange.400">{project.framework}</Badge>
                            {project.complexity && (
                              <Badge size="sm" variant="outline" borderColor="orange.400" color="orange.400">{project.complexity}</Badge>
                            )}
                          </HStack>
                        )}
                      </VStack>
                    </Box>
                  ))}
                  {projectHistory.length === 0 && (
                    <Text color="gray.500" fontSize="sm" textAlign="center">
                      No projects generated yet
                    </Text>
                  )}
                </VStack>
              </Box>

              {/* File Preview */}
              {selectedFile && (
                <Box>
                  <HStack mb={4}>
                    <FileText size={20} color="#ff8c00" />
                    <Heading size="md" bgGradient="linear(to-r, orange.400, yellow.400)" bgClip="text">File Preview</Heading>
                  </HStack>
                  <Box
                    bg="black"
                    p={4}
                    borderRadius="md"
                    fontFamily="mono"
                    fontSize="sm"
                    maxH="400px"
                    overflowY="auto"
                  >
                    <Text color="gray.300">
                      {generatedFiles.find(f => f.name === selectedFile)?.content}
                    </Text>
                  </Box>
                </Box>
              )}
            </VStack>
          </Box>
        </Flex>
      </Box>
    </ChakraProvider>
  );
}

export default App;
  