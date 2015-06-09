class Reading < ActiveRecord::Base
    def self.getbill(type, sector, location)
        if type == "gas"
            if location == "All"
                finalresult = []
                firstresult = self.where('business_class = ? and gas_billed IS NOT NULL', sector)
                firstresult.each do |x|
                    if finalresult.present? and finalresult.include?(x.read_date)
                        finalresult.last.gas_billed += x.gas_billed
                    else
                        finalresult += [x]
                    end
                end
                result = finalresult
            else
                result = self.where('business_class = ? and gas_billed IS NOT NULL and city_code = ?', sector, location.upcase)
            end
        elsif type == "electric"
            if location == "All"
                finalresult = []
                firstresult = self.where('business_class = ? and electric_billed IS NOT NULL', sector)
                firstresult.each do |x|
                    if finalresult.present? and finalresult.include?(x.read_date)
                        finalresult.last.electric_billed += x.electric_billed
                    else
                        finalresult += [x]
                    end
                end
                result = finalresult
            else
                result = self.where('business_class = ? and electric_billed IS NOT NULL and city_code = ?', sector, location.upcase)
            end
        end
        return result
    end
    
    def self.billsum(type, twp, boro)
        if type == "gas"
            result = twp.pluck(:gas_billed).sum + boro.pluck(:gas_billed).sum
        elsif type == "electric"
            result = twp.pluck(:electric_billed).sum + boro.pluck(:electric_billed).sum
        elsif type == "All"
            result = self.where('business_class = ? and electric_billed IS NOT NULL', sector)
        end
        return result
    end
    
    def self.yeardaterange(data, startdate, enddate)
        result = data.where(read_date: DateTime.new(startdate)..(DateTime.new(enddate) - 1.month))
        result = result.pluck(:read_date).map{|readdate| readdate.strftime("%B, %Y").gsub(/,/, '')}
        return result
    end
    
    def self.yeardatarange(data, type, startdate, enddate)
        result = data.where(read_date: DateTime.new(startdate)..(DateTime.new(enddate) - 1.month))
        if type == "gas"
            result = result.pluck(:gas_billed)
        elsif type == "electric"
            result = result.pluck(:electric_billed)
        end
        return result
    end
    
    def self.thmtokwh(x)
        x * 29.3001111
    end
end
