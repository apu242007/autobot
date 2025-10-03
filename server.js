import express from 'express';
import dotenv from 'dotenv';
import cors from 'cors';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import axios from 'axios';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;
const PYTHON_API_URL = process.env.PYTHON_API_URL || 'http://localhost:5000';

// Middleware de seguridad
app.use(helmet());
app.use(cors());
app.use(express.json());

// Rate limiting
const limiter = rateLimit({
  windowMs: parseInt(process.env.RATE_LIMIT_WINDOW_MS) || 15 * 60 * 1000,
  max: parseInt(process.env.RATE_LIMIT_MAX_REQUESTS) || 100,
  message: 'Demasiadas solicitudes desde esta IP, intente más tarde.'
});
app.use('/api/', limiter);

// Logging middleware
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
  next();
});

// Health check
app.get('/health', (_, res) => {
  res.json({ 
    status: 'ok',
    timestamp: new Date().toISOString(),
    service: 'autobot-nodejs-api',
    version: '1.0.0'
  });
});

// Iniciar evaluación
app.post('/api/evaluation/start', async (req, res) => {
  try {
    const { channel, personality } = req.body;
    
    if (!channel || !personality) {
      return res.status(400).json({
        error: 'Los campos channel y personality son requeridos'
      });
    }

    const response = await axios.post(`${PYTHON_API_URL}/api/evaluation/start`, {
      channel,
      personality
    });

    res.json(response.data);
  } catch (error) {
    console.error('Error al iniciar evaluación:', error.message);
    res.status(error.response?.status || 500).json({
      error: error.response?.data?.error || 'Error al iniciar evaluación'
    });
  }
});

// Enviar respuesta del agente
app.post('/api/evaluation/:id/respond', async (req, res) => {
  try {
    const { id } = req.params;
    const { agent_response } = req.body;

    if (!agent_response) {
      return res.status(400).json({
        error: 'El campo agent_response es requerido'
      });
    }

    const response = await axios.post(
      `${PYTHON_API_URL}/api/evaluation/${id}/respond`,
      { agent_response }
    );

    res.json(response.data);
  } catch (error) {
    console.error('Error al procesar respuesta:', error.message);
    res.status(error.response?.status || 500).json({
      error: error.response?.data?.error || 'Error al procesar respuesta'
    });
  }
});

// Finalizar evaluación
app.post('/api/evaluation/:id/finalize', async (req, res) => {
  try {
    const { id } = req.params;

    const response = await axios.post(
      `${PYTHON_API_URL}/api/evaluation/${id}/finalize`
    );

    res.json(response.data);
  } catch (error) {
    console.error('Error al finalizar evaluación:', error.message);
    res.status(error.response?.status || 500).json({
      error: error.response?.data?.error || 'Error al finalizar evaluación'
    });
  }
});

// Obtener reporte de evaluación
app.get('/api/evaluation/:id/report', async (req, res) => {
  try {
    const { id } = req.params;

    const response = await axios.get(
      `${PYTHON_API_URL}/api/evaluation/${id}/report`
    );

    res.json(response.data);
  } catch (error) {
    console.error('Error al obtener reporte:', error.message);
    res.status(error.response?.status || 500).json({
      error: error.response?.data?.error || 'Error al obtener reporte'
    });
  }
});

// Obtener puntaje actual
app.get('/api/evaluation/:id/score', async (req, res) => {
  try {
    const { id } = req.params;

    const response = await axios.get(
      `${PYTHON_API_URL}/api/evaluation/${id}/score`
    );

    res.json(response.data);
  } catch (error) {
    console.error('Error al obtener puntaje:', error.message);
    res.status(error.response?.status || 500).json({
      error: error.response?.data?.error || 'Error al obtener puntaje'
    });
  }
});

// Listar evaluaciones
app.get('/api/evaluations', async (req, res) => {
  try {
    const response = await axios.get(`${PYTHON_API_URL}/api/evaluations`);
    res.json(response.data);
  } catch (error) {
    console.error('Error al listar evaluaciones:', error.message);
    res.status(error.response?.status || 500).json({
      error: error.response?.data?.error || 'Error al listar evaluaciones'
    });
  }
});

// Error 404
app.use((req, res) => {
  res.status(404).json({ error: 'Endpoint no encontrado' });
});

// Manejo de errores global
app.use((err, req, res, next) => {
  console.error('Error global:', err);
  res.status(500).json({ error: 'Error interno del servidor' });
});

app.listen(PORT, () => {
  console.log(`🟢 API Node.js escuchando en http://localhost:${PORT}`);
  console.log(`🐍 Python API configurada en: ${PYTHON_API_URL}`);
  console.log(`⚙️  Ambiente: ${process.env.NODE_ENV || 'development'}`);
});
