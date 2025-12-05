from django.test import TestCase
from rest_framework.test import APIRequestFactory
from types import SimpleNamespace
from unittest.mock import patch, MagicMock
import io

from api import views as views_module


class EndpointTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_registro_usuario(self):
        request = self.factory.post("/api/registro_usuario/", {}, format="json")
        with patch(
            "api.views.usuario_service.registrar_usuario",
            return_value=SimpleNamespace(),
        ):
            with patch(
                "api.views.UsuarioSerializer",
                return_value=SimpleNamespace(data={"id": 1}),
            ):
                resp = views_module.registro_usuario(request)
                self.assertEqual(resp.status_code, 201)

    def test_obtener_usuario(self):
        request = self.factory.get("/api/usuario/1/")
        with patch(
            "api.views.usuario_service.obtener_usuario", return_value=SimpleNamespace()
        ):
            with patch(
                "api.views.UsuarioSerializer",
                return_value=SimpleNamespace(data={"id": 1}),
            ):
                resp = views_module.obtener_usuario(request, 1)
                self.assertEqual(resp.status_code, 200)

    def test_mostrar_sendero(self):
        request = self.factory.get("/api/sendero/1/")
        with patch(
            "api.views.sendero_service.obtener_sendero", return_value=SimpleNamespace()
        ):
            with patch(
                "api.views.SenderoSerializer",
                return_value=SimpleNamespace(data={"id": 1}),
            ):
                resp = views_module.mostrar_sendero(request, 1)
                self.assertEqual(resp.status_code, 200)

    def test_listar_senderos(self):
        request = self.factory.get("/api/senderos/")
        with patch(
            "api.views.sendero_service.listar_todos_los_senderos",
            return_value=[SimpleNamespace()],
        ):
            with patch(
                "api.views.SenderoSerializer",
                return_value=SimpleNamespace(data=[{"id": 1}]),
            ):
                resp = views_module.listar_senderos(request)
                self.assertEqual(resp.status_code, 200)

    def test_mostrar_foto_sendero(self):
        request = self.factory.get("/api/foto-sendero/1/")
        with patch(
            "api.views.foto_sendero_service.obtener_foto_sendero",
            return_value=SimpleNamespace(),
        ):
            with patch(
                "api.views.SenderoFotoSerializer",
                return_value=SimpleNamespace(data={"id": 1}),
            ):
                resp = views_module.mostrar_foto_sendero(request, 1)
                self.assertEqual(resp.status_code, 200)

    def test_listar_fotos_senderos(self):
        request = self.factory.get("/api/fotos-senderos/")
        with patch(
            "api.views.foto_sendero_service.obtener_todas_fotos_sendero",
            return_value=[SimpleNamespace()],
        ):
            with patch(
                "api.views.SenderoFotoSerializer",
                return_value=SimpleNamespace(data=[{"id": 1}]),
            ):
                resp = views_module.listar_fotos_senderos(request)
                self.assertEqual(resp.status_code, 200)

    def test_login_usuario(self):
        request = self.factory.post(
            "/api/login/", {"email": "a@b.com", "contraseña": "x"}, format="json"
        )
        with patch(
            "api.views.usuario_service.autenticar_usuario",
            return_value=({"token": "t"}, None),
        ):
            resp = views_module.login_usuario(request)
            self.assertEqual(resp.status_code, 200)

    def test_registrar_encuesta_view(self):
        request = self.factory.post("/api/encuesta/", {"q": 1}, format="json")
        with patch(
            "api.views.encuesta_service.registrar_encuesta",
            return_value=(SimpleNamespace(), None),
        ):
            resp = views_module.registrar_encuesta_view(request)
            self.assertEqual(resp.status_code, 201)

    def test_agregar_comentario(self):
        request = self.factory.post("/api/comentario/", {"texto": "x"}, format="json")
        mock_serializer = MagicMock()
        mock_serializer.is_valid = MagicMock()
        mock_serializer.save = MagicMock(return_value=SimpleNamespace())
        mock_serializer.data = {"id": 1}
        with patch("api.views.ComentarioSerializer", return_value=mock_serializer):
            resp = views_module.agregar_comentario(request)
            self.assertEqual(resp.status_code, 201)

    def test_comentarios_por_sendero(self):
        request = self.factory.get("/api/comentarios/1/")
        with patch(
            "api.views.comentario_service.listar_comentarios_por_sendero",
            return_value=[SimpleNamespace()],
        ):
            with patch(
                "api.views.ComentarioSerializer",
                return_value=SimpleNamespace(data=[{"id": 1}]),
            ):
                resp = views_module.comentarios_por_sendero(request, 1)
                self.assertEqual(resp.status_code, 200)

    def test_valoracion_promedio(self):
        request = self.factory.get("/api/valoracion-promedio/1/")
        with patch(
            "api.views.valoracion_service.obtener_valoracion_promedio", return_value=4.5
        ):
            resp = views_module.valoracion_promedio(request, 1)
            self.assertEqual(resp.status_code, 200)

    def test_valoraciones_por_sendero(self):
        request = self.factory.get("/api/valoraciones/1/")
        with patch(
            "api.views.valoracion_service.obtener_valoraciones_por_sendero",
            return_value=[{"v": 5}],
        ):
            resp = views_module.valoraciones_por_sendero(request, 1)
            self.assertEqual(resp.status_code, 200)

    def test_obtener_visitante_por_cedula(self):
        request = self.factory.get("/api/visitante/ABC123/")
        m = MagicMock()
        m.first.return_value = SimpleNamespace(id=1)
        with patch("api.views.Visitante.objects.filter", return_value=m):
            with patch(
                "api.views.VisitanteSerializer",
                return_value=SimpleNamespace(data={"id": 1}),
            ):
                resp = views_module.obtener_visitante_por_cedula(request, "ABC123")
                self.assertEqual(resp.status_code, 200)

    def test_registrar_visita(self):
        data = {
            "cedula_pasaporte": "ABC",
            "sendero_visitado": "S1",
            "razon_visita": "x",
        }
        request = self.factory.post("/api/registrar-visita/", data, format="json")
        m_visit = MagicMock()
        m_visit.first.return_value = SimpleNamespace(id=1)
        m_sender = MagicMock()
        m_sender.first.return_value = SimpleNamespace(nombre_sendero="S1")
        with patch("api.views.Visitante.objects.filter", return_value=m_visit):
            with patch("api.views.Sendero.objects.filter", return_value=m_sender):
                with patch(
                    "api.views.RegistroVisita.objects.create",
                    return_value=SimpleNamespace(),
                ):
                    resp = views_module.registrar_visita(request)
                    self.assertEqual(resp.status_code, 201)

    def test_registrar_visitante_y_visita(self):
        data = {
            "cedula_pasaporte": "C",
            "nombre_visitante": "N",
            "nacionalidad": "P",
            "adulto_nino": "A",
            "telefono": "T",
            "genero": "G",
            "sendero_visitado": "S",
            "razon_visita": "R",
        }
        request = self.factory.post(
            "/api/registrar-visitante-visita/", data, format="json"
        )
        m_sender = MagicMock()
        m_sender.first.return_value = SimpleNamespace(nombre_sendero="S")
        with patch("api.views.Sendero.objects.filter", return_value=m_sender):
            with patch(
                "api.views.Visitante.objects.filter",
                return_value=MagicMock(exists=MagicMock(return_value=False)),
            ):
                with patch(
                    "api.views.Visitante.objects.create", return_value=SimpleNamespace()
                ):
                    with patch(
                        "api.views.RegistroVisita.objects.create",
                        return_value=SimpleNamespace(),
                    ):
                        resp = views_module.registrar_visitante_y_visita(request)
                        self.assertEqual(resp.status_code, 201)

    def test_registrar_visita_por_id(self):
        data = {"visitante_id": 1, "sendero_visitado": "S", "razon_visita": "R"}
        request = self.factory.post(
            "/api/registrar-visita-por-id/", data, format="json"
        )
        with patch(
            "api.views.Visitante.objects.get", return_value=SimpleNamespace(id=1)
        ):
            m_sender = MagicMock()
            m_sender.first.return_value = SimpleNamespace(nombre_sendero="S")
            with patch("api.views.Sendero.objects.filter", return_value=m_sender):
                with patch(
                    "api.views.RegistroVisita.objects.create",
                    return_value=SimpleNamespace(),
                ):
                    resp = views_module.registrar_visita_por_id(request)
                    self.assertEqual(resp.status_code, 201)

    def test_visitas_recientes(self):
        request = self.factory.get("/api/visitas-recientes/")
        with patch(
            "api.views.dashboard_service.obtener_visitas_recientes",
            return_value=[{"v": 1}],
        ):
            resp = views_module.visitas_recientes(request)
            self.assertEqual(resp.status_code, 200)

    def test_visitantes_hoy(self):
        request = self.factory.get("/api/visitantes-hoy/")
        with patch("api.views.dashboard_service.contar_visitantes_hoy", return_value=5):
            resp = views_module.visitantes_hoy(request)
            self.assertEqual(resp.status_code, 200)

    def test_encuestas_hoy(self):
        request = self.factory.get("/api/encuestas-hoy/")
        with patch("api.views.dashboard_service.contar_encuestas_hoy", return_value=3):
            resp = views_module.encuestas_hoy(request)
            self.assertEqual(resp.status_code, 200)

    def test_visitantes_por_pais(self):
        request = self.factory.get("/api/visitantes-por-pais/")
        with patch(
            "api.views.dashboard_service.obtener_visitantes_por_pais",
            return_value=[{"pais": "P", "count": 1}],
        ):
            resp = views_module.visitantes_por_pais(request)
            self.assertEqual(resp.status_code, 200)

    def test_visitantes_por_sendero(self):
        request = self.factory.get("/api/visitantes-por-sendero/")
        with patch(
            "api.views.dashboard_service.obtener_visitantes_por_sendero",
            return_value=[{"sendero": "S", "count": 1}],
        ):
            resp = views_module.visitantes_por_sendero(request)
            self.assertEqual(resp.status_code, 200)

    def test_reporte_excel(self):
        request = self.factory.get("/api/reporte-excel/")
        fake_file = io.BytesIO(b"xlscontent")
        with patch("api.views.generar_reporte_completo", return_value=fake_file):
            resp = views_module.reporte_excel(request)
            # HttpResponse from view; status_code for successful file is 200
            self.assertEqual(resp.status_code, 200)
