package org

import future.keywords
import data.circleci.config

policy_name["mandate_sast_orb"]

require_orbs_versioned = config.require_orbs_version(["snyk/snyk@1.1.2"])

enable_rule["require_orbs_versioned"]

hard_fail["require_orbs_versioned"] {
	require_orbs_versioned
}