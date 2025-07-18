from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import whois
import re
from typing import Dict, Any

router = APIRouter()

class DomainRequest(BaseModel):
    domain: str

class WhoisService:
    @staticmethod
    def is_valid_domain(domain: str) -> bool:
        """
        Validate if the input is a valid domain name format.
        Accepts formats like: example.com, sub.example.com, etc.
        """
        # Basic domain validation pattern
        domain_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
        
        if not domain or len(domain) > 253:
            return False
            
        # Check if domain has at least one dot
        if '.' not in domain:
            return False
            
        # Check pattern match
        if not re.match(domain_pattern, domain):
            return False
            
        # Check each label length (max 63 characters)
        labels = domain.split('.')
        for label in labels:
            if len(label) > 63 or len(label) == 0:
                return False
                
        return True
    
    @staticmethod
    def perform_whois_lookup(domain: str) -> Dict[str, Any]:
        """
        Perform WHOIS lookup for the given domain.
        """
        try:
            result = whois.whois(domain)
            
            # Convert the result to a serializable format
            whois_data = {}
            
            # Handle common whois fields
            fields_to_extract = [
                'domain_name', 'registrar', 'whois_server', 'referral_url',
                'updated_date', 'creation_date', 'expiration_date', 'name_servers',
                'status', 'emails', 'dnssec', 'name', 'org', 'address', 'city',
                'state', 'zipcode', 'country'
            ]
            
            for field in fields_to_extract:
                if hasattr(result, field):
                    value = getattr(result, field)
                    # Convert datetime objects to strings
                    if hasattr(value, 'strftime'):
                        whois_data[field] = value.strftime('%Y-%m-%d %H:%M:%S')
                    elif isinstance(value, list):
                        # Handle lists (like name_servers, emails)
                        whois_data[field] = [str(item) for item in value if item]
                    elif value:
                        whois_data[field] = str(value)
            
            return whois_data
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"WHOIS lookup failed: {str(e)}"
            )

@router.get("/whois")
async def whois_lookup(domain: str):
    """
    Perform WHOIS lookup for a domain.
    
    Args:
        domain: The domain name to lookup (e.g., example.com)
    
    Returns:
        JSON response with WHOIS information
    """
    if not domain:
        raise HTTPException(
            status_code=400,
            detail="Domain parameter is required"
        )
    
    # Validate domain format
    if not WhoisService.is_valid_domain(domain):
        raise HTTPException(
            status_code=400,
            detail="Invalid domain format. Expected format: example.com"
        )
    
    # Perform WHOIS lookup
    whois_data = WhoisService.perform_whois_lookup(domain)
    
    return {
        "domain": domain,
        "whois_data": whois_data,
        "status": "success"
    }
