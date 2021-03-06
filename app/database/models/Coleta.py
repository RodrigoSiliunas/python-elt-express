from ast import Str
from enum import unique
from sqlalchemy import Column, Integer, String, DateTime
from app.database.models import DeclarativeBase


class Coleta(DeclarativeBase.Model):
    __tablename__ = 'coletas'

    id                                      = Column(Integer, primary_key=True, autoincrement=True)
    esl_id                                  = Column(Integer)
    reference_number                        = Column(String(150))
    modal                                   = Column(String(150))
    service_at                              = Column(DateTime)
    taxed_weight                            = Column(String(150))
    km                                      = Column(String(150))
    freight_weight_subtotal                 = Column(String(150))
    adm_fee_subtotal                        = Column(String(150))
    other_fees                              = Column(String(150))
    total                                   = Column(String(150))
    comments                                = Column(String(150))
    service_type                            = Column(String(150))
    emission_type                           = Column(String(150))
    corporation_sequence_number             = Column(Integer)
    total_cubic_volume                      = Column(String(150))
    invoices_volumes                        = Column(Integer)
    invoices_value                          = Column(String(150))
    gris_subtotal                           = Column(String(150))
    ad_valorem_subtotal                     = Column(String(150))
    invoices_weight                         = Column(String(150))
    type                                    = Column(String(150))
    fit_ant_document                        = Column(String(150))
    fit_crn_psn_nickname                    = Column(String(150))
    fit_ccr_name                            = Column(String(150))
    fit_cre_code                            = Column(String(150))
    fit_cre_name                            = Column(String(150))
    fit_cre_range_type                      = Column(String(150))
    fit_dpn_delivery_prediction_at          = Column(DateTime)
    fit_f_l_tax_value                       = Column(String(150))
    fit_fte_foe_occurrence_at               = Column(DateTime)
    fit_fte_foe_ore_description             = Column(String(150))
    fit_fte_lce_receiver                    = Column(String(150))
    fit_fte_lce_ore_description             = Column(String(150))
    fit_fsn_name                            = Column(String(150))
    fit_fhe_cte_number                      = Column(Integer)
    fit_fhe_cte_created_at                  = Column(DateTime)
    fit_fis_freight_total_by_invoice_weight = Column(String(150))
    fit_fis_ioe_number                      = Column(String(150))
    fit_fis_ioe_order_number                = Column(String(150))
    fit_fis_ioe_volume                      = Column(Integer)
    fit_fis_ioe_value                       = Column(String(150))
    fit_fis_ioe_key                         = Column(String(150))
    fit_mey_mft_sequence_code               = Column(Integer)
    fit_o_t_additionals_subtotal            = Column(String(150))
    fit_o_t_ad_valorem_subtotal             = Column(String(150))
    fit_o_t_gris_subtotal                   = Column(String(150))
    fit_p_m_pck_finish_date                 = Column(String(150))
    fit_rpt_nickname                        = Column(String(150))
    fit_rpt_document                        = Column(String(150))
    fit_rpt_code                            = Column(String(150))
    fit_rpt_cor_psn_mobile_operator         = Column(String(150))
    fit_rpt_mds_cty_name                    = Column(String(150))
    fit_rpt_mds_cty_sae_code                = Column(String(150))
    fit_sdr_nickname                        = Column(String(150))
    fit_sdr_document                        = Column(String(150))
    fit_sdr_code                            = Column(String(150))
    fit_sdr_mds_cty_name                    = Column(String(150))
    fit_sdr_mds_cty_sae_code                = Column(String(150))
    fit_vee_name                            = Column(String(150))
    fit_fis_id                              = Column(Integer, unique=True)
    fit_pyr_nickname                        = Column(String(150))
    fit_rir_nickname                        = Column(String(150))
    fit_p_m_pck_mik_mft_sequence_code       = Column(String(150))
    fit_rir_document                        = Column(String(150))
    fit_rir_code                            = Column(String(150))

    @classmethod
    def _add_column(cls, column, value):
        setattr(cls, column, value)

    def _keys(self):
        return [field.name for field in self.__table__.columns]

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

