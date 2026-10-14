"""
Tests unitarios para el módulo de validadores.
"""
import pytest
from validators import InputValidator


class TestInputValidator:
    """Tests para la clase InputValidator."""
    
    def setup_method(self):
        """Setup antes de cada test."""
        self.validator = InputValidator()
    
    def test_sanitize_search_query_normal(self):
        """Test con consulta normal."""
        result = self.validator.sanitize_search_query("Python tutorial")
        assert result == "Python tutorial"
    
    def test_sanitize_search_query_malicious(self):
        """Test con caracteres maliciosos."""
        result = self.validator.sanitize_search_query("test<script>alert(1)</script>")
        assert "<script>" not in result
        assert "alert" not in result
    
    def test_sanitize_search_query_empty(self):
        """Test con consulta vacía."""
        result = self.validator.sanitize_search_query("")
        assert result is None
    
    def test_sanitize_search_query_too_long(self):
        """Test con consulta muy larga."""
        long_query = "a" * 300
        result = self.validator.sanitize_search_query(long_query)
        assert len(result) <= 200
    
    def test_validate_url_valid(self):
        """Test con URL válida."""
        assert self.validator.validate_url("https://www.google.com")
        assert self.validator.validate_url("http://example.com")
    
    def test_validate_url_local(self):
        """Test con URL local (debe rechazar)."""
        assert not self.validator.validate_url("http://localhost:8080")
        assert not self.validator.validate_url("http://127.0.0.1")
    
    def test_validate_url_invalid_scheme(self):
        """Test con esquema inválido."""
        assert not self.validator.validate_url("ftp://example.com")
        assert not self.validator.validate_url("file:///etc/passwd")
    
    def test_sanitize_filename_normal(self):
        """Test con nombre normal."""
        result = self.validator.sanitize_filename("mi_reporte")
        assert result == "mi_reporte"
    
    def test_sanitize_filename_path_traversal(self):
        """Test con intento de path traversal."""
        result = self.validator.sanitize_filename("../../etc/passwd")
        assert ".." not in result
        assert "/" not in result
    
    def test_sanitize_filename_special_chars(self):
        """Test con caracteres especiales."""
        result = self.validator.sanitize_filename("reporte#$%@!.txt")
        assert "#" not in result
        assert "$" not in result
    
    def test_sanitize_html_content(self):
        """Test con contenido HTML."""
        html = "<p>Hola</p><script>alert(1)</script>"
        result = self.validator.sanitize_html_content(html)
        assert "<script>" not in result
        assert "Hola" in result
