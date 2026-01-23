/**
 * API Client for Sistema de Ordens de Serviço
 */

const API_BASE_URL = window.location.origin.includes('localhost') || window.location.origin.includes('127.0.0.1')
    ? 'http://localhost:8000/api/v1'
    : window.location.origin + '/api/v1';

class APIClient {
    constructor() {
        this.token = localStorage.getItem('access_token');
        this.user = JSON.parse(localStorage.getItem('user') || 'null');
    }

    /**
     * Get authorization headers
     */
    getHeaders() {
        const headers = {
            'Content-Type': 'application/json',
        };

        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }

        return headers;
    }

    /**
     * Handle API response
     */
    async handleResponse(response) {
        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'Erro desconhecido' }));
            throw new Error(error.detail || `Erro ${response.status}`);
        }

        // No content responses
        if (response.status === 204) {
            return null;
        }

        return response.json();
    }

    /**
     * Authentication
     */
    async login(username, password) {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password }),
        });

        const data = await this.handleResponse(response);

        // Store token and user
        this.token = data.access_token;
        this.user = data.user;
        localStorage.setItem('access_token', this.token);
        localStorage.setItem('user', JSON.stringify(this.user));

        return data;
    }

    logout() {
        this.token = null;
        this.user = null;
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
        window.location.href = 'index.html';
    }

    isAuthenticated() {
        return !!this.token;
    }

    getUser() {
        return this.user;
    }

    /**
     * Ordens de Serviço
     */
    async getOrdensList(filters = {}) {
        const params = new URLSearchParams();

        if (filters.status) params.append('status_filter', filters.status);
        if (filters.tipo_os) params.append('tipo_os', filters.tipo_os);
        if (filters.tecnico_executor_id) params.append('tecnico_executor_id', filters.tecnico_executor_id);
        if (filters.limit) params.append('limit', filters.limit);
        if (filters.offset) params.append('offset', filters.offset);

        const queryString = params.toString();
        const url = `${API_BASE_URL}/os${queryString ? '?' + queryString : ''}`;

        const response = await fetch(url, {
            headers: this.getHeaders(),
        });

        return this.handleResponse(response);
    }

    async getOrdensRompimentoManutencao() {
        // Buscar O.S de rompimento e manutenções
        const [rompimento, manutencao] = await Promise.all([
            this.getOrdensList({ tipo_os: 'rompimento', limit: 100 }),
            this.getOrdensList({ tipo_os: 'manutencao', limit: 100 })
        ]);
        return [...rompimento, ...manutencao];
    }

    async getOrdemById(id) {
        const response = await fetch(`${API_BASE_URL}/os/${id}`, {
            headers: this.getHeaders(),
        });

        return this.handleResponse(response);
    }

    async assumirOrdem(id, tecnicoExecutorId) {
        const response = await fetch(`${API_BASE_URL}/os/${id}/assumir`, {
            method: 'PATCH',
            headers: this.getHeaders(),
            body: JSON.stringify({ tecnico_executor_id: tecnicoExecutorId }),
        });

        return this.handleResponse(response);
    }

    async finalizarOrdem(id, fotoComprovacao, observacoes = null) {
        const response = await fetch(`${API_BASE_URL}/os/${id}/finalizar`, {
            method: 'PATCH',
            headers: this.getHeaders(),
            body: JSON.stringify({
                foto_comprovacao: fotoComprovacao,
                observacoes: observacoes,
            }),
        });

        return this.handleResponse(response);
    }

    async finalizarOrdemComFoto(id, fotoFile, observacoes = null) {
        // Create FormData to send file
        const formData = new FormData();
        formData.append('foto_comprovacao', fotoFile);
        if (observacoes) {
            formData.append('observacoes', observacoes);
        }

        const response = await fetch(`${API_BASE_URL}/os/${id}/finalizar-com-foto`, {
            method: 'PATCH',
            headers: {
                'Authorization': `Bearer ${this.token}`,
                // Don't set Content-Type, browser will set it with boundary for multipart/form-data
            },
            body: formData,
        });

        return this.handleResponse(response);
    }

    async updateOrdem(id, updates) {
        const response = await fetch(`${API_BASE_URL}/os/${id}`, {
            method: 'PATCH',
            headers: this.getHeaders(),
            body: JSON.stringify(updates),
        });

        return this.handleResponse(response);
    }

    async deleteOrdem(id) {
        const response = await fetch(`${API_BASE_URL}/os/${id}`, {
            method: 'DELETE',
            headers: this.getHeaders(),
        });

        return this.handleResponse(response);
    }

    /**
     * Dashboard / Reports
     */
    async getDashboard() {
        const response = await fetch(`${API_BASE_URL}/relatorios/dashboard`, {
            headers: this.getHeaders(),
        });

        return this.handleResponse(response);
    }

    /**
     * Gestão de Usuários (Admin only)
     */
    async getUsuarios() {
        const response = await fetch(`${API_BASE_URL}/usuarios`, {
            headers: this.getHeaders(),
        });
        return this.handleResponse(response);
    }

    async createUsuario(userData) {
        const response = await fetch(`${API_BASE_URL}/usuarios`, {
            method: 'POST',
            headers: this.getHeaders(),
            body: JSON.stringify(userData),
        });
        return this.handleResponse(response);
    }

    async updateUsuario(id, userData) {
        const response = await fetch(`${API_BASE_URL}/usuarios/${id}`, {
            method: 'PATCH',
            headers: this.getHeaders(),
            body: JSON.stringify(userData),
        });
        return this.handleResponse(response);
    }

    async deleteUsuario(id) {
        const response = await fetch(`${API_BASE_URL}/usuarios/${id}`, {
            method: 'DELETE',
            headers: this.getHeaders(),
        });
        return this.handleResponse(response);
    }
}

// Create global instance
const api = new APIClient();

// Auth guard for pages
function requireAuth() {
    if (!api.isAuthenticated()) {
        window.location.href = 'index.html';
        return false;
    }
    return true;
}

// Role check
function hasRole(...roles) {
    const user = api.getUser();
    return user && roles.includes(user.role);
}
