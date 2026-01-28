# -*- coding: utf-8 -*-
import json
import logging
from odoo.addons.base.models import ir_ui_view

_logger = logging.getLogger(__name__)

def post_load_hook():
    """Hook para instrumentar el renderizado de templates y diagnosticar el problema del footer"""
    
    # Instrumentar _combine para ver qué templates se están aplicando
    original_combine = ir_ui_view.IrUiView._combine
    
    def _combine_instrumented(self, hierarchy):
        # #region agent log
        try:
            import time
            with open('/home/odoo/.cursor/debug.log', 'a') as f:
                f.write(json.dumps({
                    'sessionId': 'debug-session',
                    'runId': 'run1',
                    'hypothesisId': 'A',
                    'location': 'hooks.py:_combine_entry',
                    'message': 'Template being combined',
                    'data': {
                        'view_key': self.key if hasattr(self, 'key') else None,
                        'view_name': self.name if hasattr(self, 'name') else None,
                        'view_id': self.id if hasattr(self, 'id') else None,
                        'active': self.active if hasattr(self, 'active') else None,
                        'priority': self.priority if hasattr(self, 'priority') else None,
                        'inherit_id': self.inherit_id.key if hasattr(self, 'inherit_id') and self.inherit_id else None,
                    },
                    'timestamp': int(time.time() * 1000)
                }) + '\n')
        except: pass
        # #endregion
        
        result = original_combine(self, hierarchy)
        
        # #region agent log
        try:
            import time
            # Contar cuántos div#footer hay en el resultado
            from lxml import etree
            if result is not None:
                footer_count = len(result.xpath("//div[@id='footer']"))
                with open('/home/odoo/.cursor/debug.log', 'a') as f:
                    f.write(json.dumps({
                        'sessionId': 'debug-session',
                        'runId': 'run1',
                        'hypothesisId': 'B',
                        'location': 'hooks.py:_combine_exit',
                        'message': 'Template combined result',
                        'data': {
                            'view_key': self.key if hasattr(self, 'key') else None,
                            'footer_div_count': footer_count,
                            'has_footer': footer_count > 0
                        },
                        'timestamp': int(time.time() * 1000)
                    }) + '\n')
        except: pass
        # #endregion
        
        return result
    
    # Reemplazar el método
    ir_ui_view.IrUiView._combine = _combine_instrumented
