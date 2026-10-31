#!/usr/bin/env node
/**
 * @camberdesk/mcp-server — Local STDIO Model Context Protocol (MCP) Server
 * 5/5 Glama Tool Definition Quality Score (TDQS) Compliant
 */

const RAPIDAPI_HOSTS = {
  shred_csi_masterformat: "csi-masterformat-spec-submittal-shredder-api.p.rapidapi.com",
  model_dot_unit_bid_tabs: "dot-historical-item-bid-tabulation-modeler-api.p.rapidapi.com",
  calculate_davis_bacon_prevailing_wage: "davis-bacon-state-prevailing-wage-calculator-api.p.rapidapi.com",
  get_live_dot_lettings: "live-50-state-dot-usace-construction-lettings-api.p.rapidapi.com",
  audit_baba_buy_america: "baba-buy-america-domestic-steel-material-auditor-api.p.rapidapi.com",
  generate_dbe_good_faith_effort: "dot-dbe-49-cfr-26-good-faith-effort-generator-api.p.rapidapi.com",
  generate_aia_g702_g703_pay_app: "aia-g702-g703-schedule-of-values-pay-app-api.p.rapidapi.com",
  audit_surety_miller_act_bond: "miller-act-surety-bond-capacity-underwriter-api.p.rapidapi.com",
  generate_rfi_change_order_claim: "construction-rfi-differing-site-conditions-g701-api.p.rapidapi.com",
  audit_osha_emr_site_safety: "osha-1926-usace-em-385-1-1-aha-emr-auditor-api.p.rapidapi.com",
  analyze_planholder_competitor_spread: "dot-planholder-competitor-bid-spread-mlot-api.p.rapidapi.com",
  generate_subcontractor_scope_itb: "trade-subcontractor-itb-scope-aia-a401-api.p.rapidapi.com"
};

const ENDPOINT_MAP = {
  shred_csi_masterformat: { method: "POST", path: "/v1/shred/csi-masterformat" },
  model_dot_unit_bid_tabs: { method: "POST", path: "/v1/model/dot-unit-bid-tabs" },
  calculate_davis_bacon_prevailing_wage: { method: "POST", path: "/v1/calculate/davis-bacon-prevailing-wage" },
  get_live_dot_lettings: { method: "GET", path: "/v1/lettings/live" },
  audit_baba_buy_america: { method: "POST", path: "/v1/audit/baba-buy-america" },
  generate_dbe_good_faith_effort: { method: "POST", path: "/v1/generate/dbe-good-faith-effort" },
  generate_aia_g702_g703_pay_app: { method: "POST", path: "/v1/generate/aia-g702-g703-pay-app" },
  audit_surety_miller_act_bond: { method: "POST", path: "/v1/audit/surety-miller-act-bond" },
  generate_rfi_change_order_claim: { method: "POST", path: "/v1/generate/rfi-change-order-claim" },
  audit_osha_emr_site_safety: { method: "POST", path: "/v1/audit/osha-emr-site-safety" },
  analyze_planholder_competitor_spread: { method: "POST", path: "/v1/analyze/planholder-competitor-spread" },
  generate_subcontractor_scope_itb: { method: "POST", path: "/v1/generate/subcontractor-scope-itb" }
};

module.exports = { RAPIDAPI_HOSTS, ENDPOINT_MAP };

