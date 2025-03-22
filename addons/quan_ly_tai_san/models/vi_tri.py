import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ViTri(models.Model):
    _name = 'vi_tri'
    _description = 'Bảng chứa thông tin vị trí'
    _rec_name = "ten_vi_tri"
    _order = 'ma_vi_tri'
    _sql_constraints = [
        ('ma_vi_tri_unique', 'unique(ma_vi_tri)', 'Mã vị trí phải là duy nhất!'),
    ]

    ma_vi_tri = fields.Char("Mã vị trí", required=True, copy=False, default="New")
    ten_vi_tri = fields.Char("Tên vị trí", required=True)
    tai_san_ids = fields.One2many(
        comodel_name='tai_san',
        inverse_name='vi_tri_hien_tai_id',
        string="Tài sản hiện tại",
        readonly=True
    )

    @api.model
    def create(self, vals):
        if vals.get('ma_vi_tri', 'New') == 'New':
            vals['ma_vi_tri'] = self.env['ir.sequence'].next_by_code('vi_tri') or 'New'
        return super(ViTri, self).create(vals)


    def action_dieu_chuyen_tai_san(self):
        for record in self:
            return {
                'name': 'điều chuyển tài sản',
                'type': 'ir.actions.act_window',
                'res_model': 'lich_su_dieu_chuyen',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_tai_san_id': record.tai_san_ids.mapped('id')[0] if record.tai_san_ids else False,
                    'default_vi_tri_id': record.id,
                },
            }