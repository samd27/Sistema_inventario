import { useEffect, useState } from 'react';
import Card from '../../components/Card';
import Button from '../../components/Button';
import { alertasAPI } from '../../services/api';
import './AlertasList.css';

const AlertasList = () => {
  const [loading, setLoading] = useState(true);
  const [runningCheck, setRunningCheck] = useState(false);
  const [error, setError] = useState('');
  const [alertas, setAlertas] = useState([]);

  const fetchAlertas = async () => {
    try {
      setLoading(true);
      setError('');
      const res = await alertasAPI.getAll();
      setAlertas(res.data.data || []);
    } catch (err) {
      setError(err?.response?.data?.error || 'No fue posible cargar alertas');
    } finally {
      setLoading(false);
    }
  };

  const triggerCheckNow = async () => {
    try {
      setRunningCheck(true);
      setError('');
      await alertasAPI.triggerCheckNow();
      await fetchAlertas();
    } catch (err) {
      setError(err?.response?.data?.error || 'No fue posible ejecutar check-now');
    } finally {
      setRunningCheck(false);
    }
  };

  useEffect(() => {
    fetchAlertas();
  }, []);

  return (
    <div className="alertas-page">
      <div className="alertas-header">
        <h1>Alertas y Notificaciones</h1>
        <p>Alertas generadas por bajo stock desde el microservicio de alertas.</p>
      </div>

      <div className="alertas-actions">
        <Button variant="primary" onClick={triggerCheckNow} disabled={runningCheck}>
          {runningCheck ? 'Ejecutando...' : 'Ejecutar verificación ahora'}
        </Button>
        <Button variant="outline" onClick={fetchAlertas} disabled={loading}>
          Recargar
        </Button>
      </div>

      {error && (
        <Card className="error-card">
          <p>{error}</p>
        </Card>
      )}

      {loading ? (
        <Card>
          <p>Cargando alertas...</p>
        </Card>
      ) : alertas.length === 0 ? (
        <Card>
          <p>No hay alertas registradas.</p>
        </Card>
      ) : (
        <div className="alertas-grid">
          {alertas.map((alerta) => (
            <Card key={alerta.id} className={`alerta-card severidad-${alerta.severidad}`}>
              <div className="alerta-top">
                <h3>{alerta.nombre_producto}</h3>
                <span className="estado-badge">{alerta.estado}</span>
              </div>
              <p>{alerta.mensaje}</p>
              <div className="alerta-meta">
                <span>Stock actual: {alerta.stock_actual}</span>
                <span>Stock minimo: {alerta.stock_minimo}</span>
                <span>Severidad: {alerta.severidad}</span>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};

export default AlertasList;
